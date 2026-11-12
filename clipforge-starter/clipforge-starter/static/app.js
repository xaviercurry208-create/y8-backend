const form = document.getElementById('clip-form');
const input = document.getElementById('video');
const filename = document.getElementById('filename');
const submit = document.getElementById('submit');
const progressWrap = document.getElementById('progress-wrap');
const progress = document.getElementById('progress');
const status = document.getElementById('status');
const result = document.getElementById('result');
input.addEventListener('change', () => { filename.textContent = input.files[0]?.name || 'No file selected'; });
form.addEventListener('submit', (event) => {
  event.preventDefault();
  if (!input.files.length) return;
  submit.disabled = true;
  progressWrap.hidden = false;
  result.hidden = true;
  progress.style.width = '0%';
  status.textContent = 'Uploading video...';
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/api/clip');
  xhr.upload.addEventListener('progress', (evt) => {
    if (evt.lengthComputable) progress.style.width = `${Math.round(evt.loaded / evt.total * 100)}%`;
    if (evt.lengthComputable && evt.loaded === evt.total) status.textContent = 'Processing video with FFmpeg...';
  });
  xhr.onload = () => {
    submit.disabled = false;
    let data = {};
    try { data = JSON.parse(xhr.responseText); } catch {}
    result.hidden = false;
    if (xhr.status >= 200 && xhr.status < 300 && data.download_url) {
      result.className = 'result';
      result.replaceChildren(document.createTextNode('Your clip is ready. '));
      const link = document.createElement('a');
      link.href = data.download_url;
      link.textContent = 'Download MP4';
      result.append(link);
      status.textContent = 'Finished!';
    } else {
      result.className = 'result error';
      result.textContent = data.error || 'Video processing failed.';
      status.textContent = 'Something went wrong.';
    }
  };
  xhr.onerror = () => {
    submit.disabled = false;
    result.hidden = false;
    result.className = 'result error';
    result.textContent = 'Could not reach the Python server.';
  };
  xhr.send(new FormData(form));
});
