/**
 * Simple WebRTC Video Call Implementation
 * 
 * This script handles the core WebRTC functionality including:
 * - Setting up local and remote media streams
 * - Creating and managing peer connections
 * - Handling signaling (via a simple localStorage implementation for demo purposes)
 * - Managing call state
 */

class WebRTCCall {
    constructor() {
      // State
      this.localStream = null;
      this.remoteStream = null;
      this.peerConnection = null;
      this.roomId = null;
      this.isInitiator = false;
      this.signalingChannel = null;
      
      // Event callbacks
      this.onStatusChange = null;
      this.onRemoteStreamAdded = null;
      this.onLocalStreamAdded = null;
      this.onRoomCreated = null;
      this.onError = null;
  
      // Configuration
      this.servers = {
        iceServers: [
          { urls: 'stun:stun.l.google.com:19302' },
          { urls: 'stun:stun1.l.google.com:19302' }
        ]
      };
    }
  
    /**
     * Initialize local media stream (camera and microphone)
     * @returns {Promise} Promise that resolves when media is initialized
     */
    async initLocalMedia() {
      try {
        console.log("Requesting camera and microphone access...");
        
        // Use more specific constraints to help with compatibility
        this.localStream = await navigator.mediaDevices.getUserMedia({ 
          video: {
            width: { ideal: 640 },
            height: { ideal: 480 },
            facingMode: "user"
          }, 
          audio: true 
        });
        
        // Log track information for debugging
        const videoTracks = this.localStream.getVideoTracks();
        const audioTracks = this.localStream.getAudioTracks();
        
        console.log("Media stream obtained:");
        console.log("- Video tracks:", videoTracks.length);
        console.log("- Audio tracks:", audioTracks.length);
        
        if (videoTracks.length > 0) {
          console.log("- Video track settings:", videoTracks[0].getSettings());
        }
        
        if (this.onLocalStreamAdded) {
          this.onLocalStreamAdded(this.localStream);
        }
        
        return this.localStream;
      } catch (error) {
        this._handleError('Failed to get user media', error);
        console.error("getUserMedia error details:", error.name, error.message);
        throw error;
      }
    }
  
    /**
     * Create or join a room for video call
     * @param {string} roomId Optional room ID to join (if empty, creates a new room)
     * @returns {Promise} Promise that resolves with the room ID
     */
    async createOrJoinRoom(roomId = '') {
      // Ensure local media is initialized
      if (!this.localStream) {
        await this.initLocalMedia();
      }
  
      try {
        // Reset any existing state
        if (this.peerConnection) {
          console.log("Closing existing peer connection before creating/joining room");
          this.peerConnection.close();
          this.peerConnection = null;
        }
  
        // Create or join room
        this.roomId = roomId.trim();
        if (!this.roomId) {
          // Create new room with random ID
          this.roomId = Math.floor(Math.random() * 1000000).toString();
          this.isInitiator = true;
          this._updateStatus('Created room. Waiting for peer...');
          console.log(`Created new room with ID: ${this.roomId}`);
          
          if (this.onRoomCreated) {
            this.onRoomCreated(this.roomId);
          }
        } else {
          this.isInitiator = false;
          this._updateStatus(`Joining room: ${this.roomId}`);
          console.log(`Joining existing room with ID: ${this.roomId}`);
        }
  
        // Setup signaling
        this.signalingChannel = this._createSignalingChannel(this.roomId);
        const messageHandler = this._handleSignalingMessage.bind(this);
        const cleanupFunc = this.signalingChannel.onmessage(messageHandler);
  
        // Store cleanup function for later
        this._signalCleanup = cleanupFunc;
  
        // Setup WebRTC
        this._setupPeerConnection();
  
        // If joining existing room, send join message
        if (!this.isInitiator) {
          console.log("Sending join message to initiator");
          this.signalingChannel.send({ type: 'join' });
        }
  
        return this.roomId;
      } catch (error) {
        this._handleError('Error creating/joining room', error);
        throw error;
      }
    }
  
    /**
     * Toggle local video track on/off
     * @returns {boolean} New state of video track (enabled/disabled)
     */
    toggleVideo() {
      if (this.localStream) {
        const videoTrack = this.localStream.getVideoTracks()[0];
        if (videoTrack) {
          videoTrack.enabled = !videoTrack.enabled;
          return videoTrack.enabled;
        }
      }
      return false;
    }
  
    /**
     * Toggle local audio track on/off
     * @returns {boolean} New state of audio track (enabled/disabled)
     */
    toggleAudio() {
      if (this.localStream) {
        const audioTrack = this.localStream.getAudioTracks()[0];
        if (audioTrack) {
          audioTrack.enabled = !audioTrack.enabled;
          return audioTrack.enabled;
        }
      }
      return false;
    }
  
    /**
     * End the call and clean up resources
     */
    hangUp() {
      console.log("Hanging up call");
      
      // Clean up signaling
      if (this._signalCleanup) {
        this._signalCleanup();
        this._signalCleanup = null;
      }
      
      // Close PeerConnection
      if (this.peerConnection) {
        this.peerConnection.close();
        this.peerConnection = null;
      }
  
      // Stop local stream
      if (this.localStream) {
        this.localStream.getTracks().forEach(track => track.stop());
        this.localStream = null;
      }
  
      // Clear remote stream
      this.remoteStream = null;
      
      // Reset state
      this.isInitiator = false;
      this.roomId = null;
      this._pendingCandidates = [];
      
      this._updateStatus('Call ended');
    }
  
    /**
     * Set up the peer connection with event handlers
     * @private
     */
    _setupPeerConnection() {
      // Create RTCPeerConnection
      this.peerConnection = new RTCPeerConnection(this.servers);
  
      // Add local tracks to the connection
      this.localStream.getTracks().forEach(track => {
        this.peerConnection.addTrack(track, this.localStream);
      });
  
      // Handle ICE candidates
      this.peerConnection.onicecandidate = event => {
        if (event.candidate) {
          this.signalingChannel.send({
            type: 'candidate',
            candidate: event.candidate
          });
        }
      };
  
      // Handle connection state changes
      this.peerConnection.onconnectionstatechange = () => {
        if (this.peerConnection.connectionState === 'connected') {
          this._updateStatus('Connected!');
        }
      };
  
      // Handle incoming tracks
      this.peerConnection.ontrack = event => {
        console.log("Remote track received:", event);
        
        if (event.streams && event.streams[0]) {
          this.remoteStream = event.streams[0];
          this._updateStatus('Remote stream connected');
          
          console.log("Remote stream details:", {
            videoTracks: this.remoteStream.getVideoTracks().length,
            audioTracks: this.remoteStream.getAudioTracks().length
          });
          
          if (this.onRemoteStreamAdded) {
            this.onRemoteStreamAdded(this.remoteStream);
          }
        } else {
          console.warn("Received track event without stream");
        }
      };
      
      // Add ice connection state monitoring for debugging
      this.peerConnection.oniceconnectionstatechange = () => {
        console.log("ICE connection state:", this.peerConnection.iceConnectionState);
        this._updateStatus(`ICE connection: ${this.peerConnection.iceConnectionState}`);
      };
      
      // Monitor signaling state
      this.peerConnection.onsignalingstatechange = () => {
        console.log("Signaling state:", this.peerConnection.signalingState);
      };
  
      // If we're the initiator, create and send the offer
      if (this.isInitiator) {
        this._createAndSendOffer();
      }
    }
  
    /**
     * Create and send WebRTC offer
     * @private
     */
    async _createAndSendOffer() {
      try {
        console.log("Creating offer");
        
        // Create offer with options for better compatibility
        const offer = await this.peerConnection.createOffer({
          offerToReceiveAudio: true,
          offerToReceiveVideo: true
        });
        
        console.log("Setting local description (offer)");
        await this.peerConnection.setLocalDescription(offer);
        
        // Wait a brief moment to allow ICE candidates to be gathered
        await new Promise(resolve => setTimeout(resolve, 500));
        
        console.log("Sending offer via signaling channel");
        this.signalingChannel.send({
          type: 'offer',
          sdp: this.peerConnection.localDescription
        });
        
        this._updateStatus('Offer sent, waiting for answer...');
      } catch (error) {
        console.error("Error in createAndSendOffer:", error);
        this._handleError('Error creating offer', error);
      }
    }
  
    /**
     * Handle incoming signaling messages
     * @private
     * @param {Object} message The signaling message
     */
    async _handleSignalingMessage(message) {
      try {
        if (message.type === 'join' && this.isInitiator) {
          // Someone joined our room, send them an offer
          console.log("Received join message, creating offer as initiator");
          await this._createAndSendOffer();
        } else if (message.type === 'offer') {
          // We received an offer, set it as remote description
          console.log("Received offer, creating answer");
          try {
            await this.peerConnection.setRemoteDescription(new RTCSessionDescription(message.sdp));
            
            // Create and send answer
            const answer = await this.peerConnection.createAnswer();
            await this.peerConnection.setLocalDescription(answer);
            this.signalingChannel.send({
              type: 'answer',
              sdp: this.peerConnection.localDescription
            });
            this._updateStatus('Received offer, sent answer');
          } catch (error) {
            console.error("Error handling offer:", error);
            this._handleError('Error processing offer', error);
          }
        } else if (message.type === 'answer') {
          // We received an answer, set it as remote description
          console.log("Received answer from peer");
          try {
            await this.peerConnection.setRemoteDescription(new RTCSessionDescription(message.sdp));
            this._updateStatus('Received answer, connection established');
          } catch (error) {
            console.error("Error handling answer:", error);
            this._handleError('Error processing answer', error);
          }
        } else if (message.type === 'candidate') {
          // We received an ICE candidate
          console.log("Received ICE candidate");
          try {
            if (this.peerConnection.remoteDescription) {
              await this.peerConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
            } else {
              console.warn("Received ICE candidate but remote description not set yet");
              // Store candidate for later
              this._pendingCandidates = this._pendingCandidates || [];
              this._pendingCandidates.push(message.candidate);
            }
          } catch (error) {
            console.error("Error adding ICE candidate:", error);
            this._handleError('Error adding ICE candidate', error);
          }
        }
      } catch (error) {
        this._handleError('Error handling signaling message', error);
      }
    }
  
    /**
     * Create a signaling channel for WebRTC negotiation
     * Note: For demo, this uses localStorage which only works on same device
     * In production, you would use a real signaling server
     * @private
     * @param {string} roomId The room ID for the channel
     * @returns {Object} Signaling channel interface
     */
    _createSignalingChannel(roomId) {
      const channelId = `webrtc-room-${roomId}`;
      const messagePrefix = `webrtc-msg-${roomId}-`;
      const self = this;
      
      // Clear any stale messages from previous sessions
      Object.keys(localStorage).forEach(key => {
        if (key.startsWith(messagePrefix)) {
          localStorage.removeItem(key);
        }
      });
  
      console.log(`Creating signaling channel for room: ${roomId}`);
      
      return {
        send: function(message) {
          // Add timestamp to make message ID unique
          const timestamp = Date.now();
          const messageId = `${messagePrefix}${timestamp}-${Math.random().toString(36).substr(2, 9)}`;
          
          // Add sender info to distinguish messages
          message.sender = self.isInitiator ? 'initiator' : 'joiner';
          message.time = timestamp;
          
          console.log(`Sending ${message.type} message:`, message);
          
          // In a real app, this would send to a server
          // For this demo, we use localStorage with unique keys
          localStorage.setItem(messageId, JSON.stringify(message));
          
          // Dispatch an event to notify other tabs
          const event = new StorageEvent('storage', {
            key: messageId
          });
          window.dispatchEvent(event);
        },
  
        onmessage: function(callback) {
          // Handle incoming messages
          const storageHandler = (event) => {
            // Skip if event doesn't have a key (our manual dispatch)
            if (!event.key) return;
            
            // Only process messages for our room
            if (event.key.startsWith(messagePrefix)) {
              try {
                const message = JSON.parse(localStorage.getItem(event.key));
                
                // Skip own messages by checking sender
                const isSelfMessage = (self.isInitiator && message.sender === 'initiator') || 
                                    (!self.isInitiator && message.sender === 'joiner');
                
                if (!isSelfMessage) {
                  console.log(`Received ${message.type} message:`, message);
                  callback(message);
                }
                
                // Clean up processed message
                localStorage.removeItem(event.key);
              } catch (error) {
                console.error('Error processing message:', error);
              }
            } else if (event.key === channelId) {
              // Support for legacy message format
              try {
                const message = JSON.parse(localStorage.getItem(channelId));
                console.log(`Received legacy message: ${message.type}`);
                localStorage.removeItem(channelId);
                callback(message);
              } catch (error) {
                console.error('Error processing legacy message:', error);
              }
            }
          };
          
          window.addEventListener('storage', storageHandler);
          
          // Return a cleanup function
          return () => {
            window.removeEventListener('storage', storageHandler);
          };
        }
      };
    }
  
    /**
     * Update status and trigger callback if exists
     * @private
     * @param {string} status The status message
     */
    _updateStatus(status) {
      if (this.onStatusChange) {
        this.onStatusChange(status);
      }
    }
  
    /**
     * Handle errors and trigger callback if exists
     * @private
     * @param {string} message Error message
     * @param {Error} error Error object
     */
    _handleError(message, error) {
      console.error(`${message}:`, error);
      const errorMessage = `${message}: ${error.message || 'Unknown error'}`;
      this._updateStatus(errorMessage);
      
      if (this.onError) {
        this.onError(errorMessage, error);
      }
    }
  }
  
  // Export the class
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = WebRTCCall;
  }