Papa.parse('data/under200_latest.csv', {
  download: true,
  header: true,
  complete: function(results) {
    const tableBody = document.querySelector('#stock-table tbody');
    results.data.forEach(row => {
      if (row.Name && row.Symbol) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${row.Name}</td>
          <td>${row.Symbol}</td>
          <td>₹${parseFloat(row.Price).toFixed(2)}</td>
          <td>${row.Volume}</td>
          <td>${row.MarketCap}</td>
          <td>${row.New === 'Yes' ? '🚀' : ''}</td>
        `;
        tableBody.appendChild(tr);
      }
    });
  }
});
document.getElementById('searchInput').addEventListener('input', function () {
  const filter = this.value.toLowerCase();
  const rows = document.querySelectorAll('#stock-table tbody tr');

  rows.forEach(row => {
    const name = row.cells[0].textContent.toLowerCase();
    const symbol = row.cells[1].textContent.toLowerCase();
    row.style.display = name.includes(filter) || symbol.includes(filter) ? '' : 'none';
  });
});
