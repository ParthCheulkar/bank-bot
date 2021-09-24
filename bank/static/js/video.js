let preview = document.getElementById("preview");
let recording = document.getElementById("recording");
let startButton = document.getElementById("startButton");
let stopButton = document.getElementById("stopButton");
let downloadButton = document.getElementById("downloadButton");
let logElement = document.getElementById("log");
let myForm = document.getElementById("myForm");
let recordingTimeMS = 6000;
let recordedBlob;
// let warn_text = document.getElementById("warn_text");
let record_text = document.getElementById("record_text");
let prompt_text = document.getElementById("prompt_text");
// let bgimg = document.getElementById("bgimg");
let recording_countdown_text = document.getElementById(
    "recording_countdown_text"
);
recording_countdown_text.style.display = "none";

// bgimg.style.display = "none";
// warn_text.style.display = "none";
recording.style.display = "none";
stopButton.style.display = "none";
record_text.style.display = "none";
downloadButton.style.display = "none";
function log(msg) {
    //logElement.innerHTML += msg + "\n";
    console.log(msg);
}

function wait(delayInMS) {
    return new Promise((resolve) => setTimeout(resolve, delayInMS));
}

function startRecording(stream, lengthInMS) {
    let recorder = new MediaRecorder(stream);
    let data = [];
    // warn_text.style.display = "block";
    recorder.ondataavailable = (event) => data.push(event.data);
    recorder.start();
    // log(recorder.state + " for " + lengthInMS / 1000 + " seconds...");

    let stopped = new Promise((resolve, reject) => {
        recorder.onstop = resolve;
        recorder.onerror = (event) => reject(event.name);
    });

    let recorded = wait(lengthInMS).then(
        () => recorder.state == "recording" && recorder.stop()
    );

    return Promise.all([stopped, recorded]).then(() => data);
}

function stop(stream) {
    stream.getTracks().forEach((track) => track.stop());
}

startButton.addEventListener(
    "click",
    function () {
        navigator.mediaDevices
            .getUserMedia({
                video: true,
                audio: false,
            })
            .then((stream) => {
                let cTime = 6;
                function triggerTimer() {
                    recording_countdown_text.style.display = "block";
                    if (cTime < 1) {
                        // document.getElementById("recording_countdown_msg").innerHTML = "Recording ended";
                        recording_countdown_text.style.display = "none";
                    } else {
                        document.getElementById("timerButton").innerHTML = cTime - 1;
                        cTime = cTime - 1;
                        setTimeout(triggerTimer, 1000);
                    }
                }
                prompt_text.style.display = "none";
                triggerTimer();
                preview.srcObject = stream;
                downloadButton.href = stream;
                preview.captureStream =
                    preview.captureStream || preview.mozCaptureStream;
                return new Promise((resolve) => (preview.onplaying = resolve));
            })
            .then(() => startRecording(preview.captureStream(), recordingTimeMS))
            .then((recordedChunks) => {
                recordedBlob = new Blob(recordedChunks, { type: "video/mp4" });
                // console.log(recordedBlob);
                recording.src = URL.createObjectURL(recordedBlob);
                // warn_text.style.display = "none";
                record_text.style.display = "block";
                downloadButton.style.display = "block";

                downloadButton.href = recording.src;
                downloadButton.download = "RecordedVideo.mp4";
                preview.style.display = "none";
                recording.style.display = "block";
                // console.log(
                //   "Successfully recorded " +
                //     recordedBlob.size +
                //     " bytes of " +
                //     recordedBlob.type +
                //     " media."
                // );
            })
            .catch((obj) => {
                console.log("Error: " + obj);
            });
    },
    false
);

startButton.addEventListener("click", function () {
    startButton.style.display = "none";
});

stopButton.addEventListener(
    "click",
    function () {
        stop(preview.srcObject);
    },
    false
);

downloadButton.addEventListener("click", (e) => {
    e.preventDefault();
    const endpt = "upload";
    const formData = new FormData();
    // console.log(recordedBlob);
    formData.append("video", recordedBlob);

    // fetch(endpt, {
    //   method: "POST",
    //   body: formData,
    // }).catch(log);
    fetch(endpt, {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.mssg === "fail") {
                alert("Please ensure video lighiting and surrounding is better.");
            } else {
                console.log("redUrl");
                window.location = data.redUrl;
            }
        });

    window.setTimeout(function () {
        window.alert(
            "Please have patience, we are processing your request, you will be redirected to another page soon"
        );
    }, 500);

    // window.setTimeout(function () {
    //   window.location = "/profile/";
    // }, 8000);
});
