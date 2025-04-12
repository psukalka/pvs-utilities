/**
 * Example of how to use the WebRTCCall class
 * 
 * This script demonstrates how to:
 * - Initialize a WebRTC call
 * - Manage UI state for video controls
 * - Handle room creation and joining
 */

// Create an instance of the WebRTCCall class
const webrtcCall = new WebRTCCall();

// Initialize UI after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Example of how you would connect UI elements to WebRTC functionality
  
  // Elements (assume these exist in your HTML)
  const localVideoElement = document.getElementById('localVideo');
  const remoteVideoElement = document.getElementById('remoteVideo');
  const createJoinButton = document.getElementById('createJoinButton');
  const roomIdInput = document.getElementById('roomId');
  const statusElement = document.getElementById('status');
  const toggleVideoButton = document.getElementById('toggleVideoButton');
  const toggleAudioButton = document.getElementById('toggleAudioButton');
  const hangupButton = document.getElementById('hangupButton');
  const refreshVideoButton = document.getElementById('refreshVideoButton');
  const currentRoomElement = document.getElementById('currentRoom');
  const videoStatusElement = document.getElementById('videoStatus');
  const connectionInfoElement = document.getElementById('connectionInfo');
  
  // Setup event listeners
  
  // Event: Create or join room button clicked
  createJoinButton.addEventListener('click', async () => {
    try {
      // Get room ID from input (empty for new room)
      const roomId = roomIdInput.value;
      
      // Create or join room
      const createdRoomId = await webrtcCall.createOrJoinRoom(roomId);
      
      // Update UI with room ID
      currentRoomElement.textContent = createdRoomId;
      
      // Show and update appropriate controls
      // This code is just for example - adapt to your UI
      document.getElementById('roomControls').classList.add('hidden');
      document.getElementById('callControls').classList.remove('hidden');
    } catch (error) {
      console.error('Failed to create/join room:', error);
    }
  });
  
  // Event: Toggle video button clicked
  toggleVideoButton.addEventListener('click', () => {
    const isVideoOn = webrtcCall.toggleVideo();
    toggleVideoButton.textContent = isVideoOn ? 'Turn Off Video' : 'Turn On Video';
  });
  
  // Event: Toggle audio button clicked
  toggleAudioButton.addEventListener('click', () => {
    const isAudioOn = webrtcCall.toggleAudio();
    toggleAudioButton.textContent = isAudioOn ? 'Mute Audio' : 'Unmute Audio';
  });
  
  // Event: Hangup button clicked
  hangupButton.addEventListener('click', () => {
    webrtcCall.hangUp();
    
    // Reset UI
    document.getElementById('roomControls').classList.remove('hidden');
    document.getElementById('callControls').classList.add('hidden');
    roomIdInput.value = '';
  });
  
  // Set up WebRTCCall event handlers
  
  // Event: Status changed
  webrtcCall.onStatusChange = (status) => {
    statusElement.textContent = status;
    
    // Update connection info
    if (webrtcCall.peerConnection) {
      const connState = webrtcCall.peerConnection.connectionState || 'unknown';
      const iceState = webrtcCall.peerConnection.iceConnectionState || 'unknown';
      const signalingState = webrtcCall.peerConnection.signalingState || 'unknown';
      
      connectionInfoElement.innerHTML = `
        <div>Connection state: <strong>${connState}</strong></div>
        <div>ICE state: <strong>${iceState}</strong></div>
        <div>Signaling state: <strong>${signalingState}</strong></div>
      `;
    }
  };
  
  // Event: Local stream added
  webrtcCall.onLocalStreamAdded = (stream) => {
    console.log("Local stream added to video element");
    localVideoElement.srcObject = stream;
    
    // Add event listeners to track video element state
    localVideoElement.onloadedmetadata = () => {
      console.log("Local video metadata loaded");
      // Force play when metadata is loaded
      localVideoElement.play().catch(e => console.error("Error playing local video:", e));
    };
    
    localVideoElement.onplay = () => console.log("Local video playback started");
    localVideoElement.onerror = (e) => console.error("Local video error:", e);
  };
  
  // Event: Remote stream added
  webrtcCall.onRemoteStreamAdded = (stream) => {
    console.log("Remote stream added to video element");
    remoteVideoElement.srcObject = stream;
    
    // Add event listeners to track video element state
    remoteVideoElement.onloadedmetadata = () => {
      console.log("Remote video metadata loaded");
      // Force play when metadata is loaded
      remoteVideoElement.play().catch(e => console.error("Error playing remote video:", e));
    };
    
    remoteVideoElement.onplay = () => console.log("Remote video playback started");
    remoteVideoElement.onerror = (e) => console.error("Remote video error:", e);
  };
  
  // Event: Room created
  webrtcCall.onRoomCreated = (roomId) => {
    currentRoomElement.textContent = roomId;
  };
  
  // Event: Error occurred
  webrtcCall.onError = (message, error) => {
    console.error('WebRTC error:', message, error);
    statusElement.textContent = message;
  };
  
  // Add refresh video button functionality
  refreshVideoButton.addEventListener('click', async () => {
    try {
      // Stop any existing streams
      if (localVideoElement.srcObject) {
        localVideoElement.srcObject.getTracks().forEach(track => track.stop());
      }
      localVideoElement.srcObject = null;
      
      // Re-initialize local media
      await webrtcCall.initLocalMedia();
      
      videoStatusElement.textContent = "Video refreshed";
    } catch (error) {
      console.error("Error refreshing video:", error);
      videoStatusElement.textContent = "Error refreshing video: " + error.message;
    }
  });
  
  // Check video status and connection info every few seconds
  setInterval(() => {
    // Update video status
    let statusText = '';
    
    if (localVideoElement.srcObject) {
      const localVideoTrack = localVideoElement.srcObject.getVideoTracks()[0];
      if (localVideoTrack) {
        statusText += `Local video: ${localVideoTrack.enabled ? 'On' : 'Off'}, `;
      } else {
        statusText += 'No local video track, ';
      }
    } else {
      statusText += 'No local stream, ';
    }
    
    if (remoteVideoElement.srcObject) {
      const remoteVideoTrack = remoteVideoElement.srcObject.getVideoTracks()[0];
      if (remoteVideoTrack) {
        statusText += `Remote video: ${remoteVideoTrack.enabled ? 'On' : 'Off'}`;
      } else {
        statusText += 'No remote video track';
      }
    } else {
      statusText += 'No remote stream';
    }
    
    videoStatusElement.textContent = statusText;
    
    // Update connection info
    if (webrtcCall.peerConnection) {
      const connState = webrtcCall.peerConnection.connectionState || 'unknown';
      const iceState = webrtcCall.peerConnection.iceConnectionState || 'unknown';
      const signalingState = webrtcCall.peerConnection.signalingState || 'unknown';
      
      connectionInfoElement.innerHTML = `
        <div>Connection state: <strong>${connState}</strong></div>
        <div>ICE state: <strong>${iceState}</strong></div>
        <div>Signaling state: <strong>${signalingState}</strong></div>
      `;
    }
  }, 2000);
  
  // Clean up on page unload
  window.addEventListener('beforeunload', () => {
    webrtcCall.hangUp();
  });
});