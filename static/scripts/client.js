document.addEventListener('DOMContentLoaded', function () {
    const videoElement = document.getElementById('video');
    const cameraButtonsContainer = document.getElementById('cameraButtons');

    function getVideoDevices() {
        navigator.mediaDevices.enumerateDevices()
            .then(function (devices) {
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                videoDevices.forEach(device => {
                    const button = document.createElement('button');
                    button.className = 'camera-button';
                    button.textContent = device.label || `Camera ${cameraButtonsContainer.children.length + 1}`;
                    button.onclick = () => startStream(device.deviceId);
                    cameraButtonsContainer.appendChild(button);
                });
            });
    }

    function startStream(deviceId) {
        const constraints = {
            video: { deviceId: deviceId ? { exact: deviceId } : undefined }
        };
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                videoElement.srcObject = stream;
                stream.getTracks().forEach(track => pc.addTrack(track, stream));
                return pc.createOffer();
            })
            .then(offer => {
                return pc.setLocalDescription(offer);
            })
            .then(() => {
                // Отправка предложения на сервер и получение ответа
                let searchParams = new URLSearchParams(window.location.search);
                let videoId = searchParams.get('vd');
                return fetch('/offer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sdp: pc.localDescription.sdp,
                        type: pc.localDescription.type,
                        video_id: videoId
                    })
                });
            })
            .then(response => response.json())
            .then(answer => {
                return pc.setRemoteDescription(new RTCSessionDescription(answer));
            });
    }

    const pc = new RTCPeerConnection({
            iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
            bundlePolicy: 'max-bundle'
        });
    pc.addEventListener('track', (evt) => {
        if (evt.track.kind === 'video') {
            videoElement.srcObject = evt.streams[0];
        }
    });

    window.addEventListener("beforeunload", () => {
        pc.getTransceivers().forEach(transceiver => transceiver.stop());
        pc.close();
    });

    getVideoDevices();
});
