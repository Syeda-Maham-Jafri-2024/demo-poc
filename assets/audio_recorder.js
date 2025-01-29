let mediaRecorder;
let recordedChunks = [];
let originalTitle = document.title;
let mediaStream;

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaStream = stream;
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            mediaRecorder.start();
            console.log("Recording started...");
            document.title = "Recording...";
        })
        .catch(error => {
            console.error("Error accessing media devices.", error);
        });
}

async function saveAudioToSpecificDirectory(blob) {
    const handle = await window.showSaveFilePicker({
        suggestedName: 'recording.wav',
        types: [{
            description: 'WAV Audio',
            accept: { 'audio/wav': ['.wav'] },
        }],
    });

    const writable = await handle.createWritable();
    await writable.write(blob);
    await writable.close();
    console.log('Audio file saved to selected directory.');

    return handle;
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
        document.title = originalTitle;

        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            console.log("Media stream stopped.");
        }

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: 'audio/wav' });
            filepath = saveAudioToSpecificDirectory(blob); //
            console.log('File Handle:', filepath);
            const url = URL.createObjectURL(blob);

            // Update the audio player with the recorded audio
            const audioPlayer = document.getElementById("audio-player");
            if (audioPlayer) {
                audioPlayer.src = url;

                // Ensure metadata is loaded to get the duration
                audioPlayer.onloadedmetadata = () => {
                    const duration = audioPlayer.duration; // Length of the audio in seconds
                    console.log(`Audio Duration: ${duration} seconds`);

                    // Optionally adjust the audio player width dynamically based on duration
                    const minWidth = 300; // Minimum width of the audio player
                    const widthPerSecond = 20; // Adjust width for each second
                    const playerWidth = Math.max(minWidth, duration * widthPerSecond);

                    audioPlayer.style.width = `${playerWidth}px`; // Adjust player width
                };

            }

            // Save the audio file for download
            const anchor = document.createElement("a");
            anchor.href = url;
            anchor.download = "recording.wav";
            anchor.click();
            console.log("Recording stopped, saved, and loaded to the audio player.");
        };
        recordedChunks = [];
    } else {
        console.log("No recording in progress.");
    }
}

