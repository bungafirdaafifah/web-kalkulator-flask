document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('btn');
  if (btn) {
    btn.addEventListener('click', function () {
      alert('Terima kasih, tombol diklik!');
    });
  }
});
