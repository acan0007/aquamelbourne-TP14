async function getData() {
  // Load the Excel file
  const response = await fetch('/dataset/data.xlsx');
  const arrayBuffer = await response.arrayBuffer();

  // Use XLSX to parse the file
  const workbook = XLSX.read(arrayBuffer, { type: 'array' });
  const firstSheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[firstSheetName];

  // Convert the sheet to JSON
  const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

  // Populate the select elements with dynamic data
  const brands = new Set();
  const categories = new Set();

  data.slice(1).forEach((row) => {
    if (row[0]) brands.add(row[0]); // Assuming brand is in the first column
    if (row[6]) categories.add(row[6]); // Assuming category is in the seventh column
  });

  const brandSelect = document.getElementById('brandSelect');
  brands.forEach((brand) => {
    const option = document.createElement('option');
    option.value = brand;
    option.textContent = brand;
    brandSelect.appendChild(option);
  });

  const categorySelect = document.getElementById('categorySelect');
  categories.forEach((category) => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
  });

  // product name search

  // slider select

  // Clear the tbody
  let tableBody = document.getElementById('tbody');
  tableBody.innerHTML = '';

  // Populate the table
  data.slice(1).forEach((row) => {
    let tableRow = `
          <tr>
              <td>${row[0]}</td>
              <td>${row[1]}</td>
              <td>${row[2]}</td>
              <td>${row[3]}</td>
              <td>${row[4]}</td>
              <td>${row[5]}</td>
              <td>${row[6]}</td>
          </tr>
      `;
    tableBody.innerHTML += tableRow;
  });

  // Initialize DataTables
  $('#NitrogenTable').DataTable({
    data: data.slice(1), // Skip the header row for DataTable
    columns: [
      { data: 0 }, // Brand
      { data: 1 }, // Product Name
      { data: 2 }, // Ingredients containing Nitrogen
      { data: 3 }, // Number of Nitrogen Ingredients
      { data: 4 }, // Total Nitrogen in Product
      { data: 5 }, // Percentage of Nitrogen Ingredients
      { data: 6 }, // Product Category
    ],
  });
}

// Call getData when the page is loaded
document.addEventListener('DOMContentLoaded', getData);

// Buttons Apply Filters and Reset Filters
document.getElementById('applyFilters').addEventListener('click', function () {
  const brand = document.getElementById('brandSelect').value;
  const category = document.getElementById('categorySelect').value;
  const productName = document
    .getElementById('productNamesearch')
    .value.toLowerCase();
  async function getData() {
    // Load the Excel file
    const response = await fetch('../dataset/data.xlsx');
    const arrayBuffer = await response.arrayBuffer();

    // Use XLSX to parse the file
    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    const firstSheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[firstSheetName];

    // Convert the sheet to JSON
    const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

    // Populate the select elements with dynamic data
    const brands = new Set();
    const categories = new Set();

    data.slice(1).forEach((row) => {
      if (row[0]) brands.add(row[0]); // Assuming brand is in the first column
      if (row[6]) categories.add(row[6]); // Assuming category is in the seventh column
    });

    const brandSelect = document.getElementById('brandSelect');
    brands.forEach((brand) => {
      const option = document.createElement('option');
      option.value = brand;
      option.textContent = brand;
      brandSelect.appendChild(option);
    });

    const categorySelect = document.getElementById('categorySelect');
    categories.forEach((category) => {
      const option = document.createElement('option');
      option.value = category;
      option.textContent = category;
      categorySelect.appendChild(option);
    });

    // Populate the table
    let tableBody = document.getElementById('tbody');
    tableBody.innerHTML = '';

    // Initialize slider
    const nitrogenSlider = document.getElementById('nitrogenSlider');
    noUiSlider.create(nitrogenSlider, {
      start: [0, 100], // Adjust based on your data's range
      connect: true,
      range: {
        min: 0,
        max: 100, // Assuming 100 is the max percentage of nitrogen
      },
      tooltips: [true, true],
    });

    // Event listener for slider change
    nitrogenSlider.noUiSlider.on('update', function (values, handle) {
      const minValue = parseFloat(values[0]);
      const maxValue = parseFloat(values[1]);
      applyFilters(minValue, maxValue);
    });

    // Populate the table body with data
    data.slice(1).forEach((row) => {
      let tableRow = `
          <tr>
            <td>${row[0]}</td> <!-- Brand -->
            <td>${row[1]}</td> <!-- Product Name -->
            <td>${row[2]}</td> <!-- Ingredients containing Nitrogen -->
            <td>${row[3]}</td> <!-- Number of Nitrogen Ingredients -->
            <td>${row[4]}</td> <!-- Total Nitrogen in Product -->
            <td>${row[5]}</td> <!-- Percentage of Nitrogen Ingredients -->
            <td>${row[6]}</td> <!-- Product Category -->
          </tr>
        `;
      tableBody.innerHTML += tableRow;
    });

    // Initialize DataTables
    $('#NitrogenTable').DataTable({
      data: data.slice(1), // Skip the header row for DataTable
      columns: [
        { data: 0 }, // Brand
        { data: 1 }, // Product Name
        { data: 2 }, // Ingredients containing Nitrogen
        { data: 3 }, // Number of Nitrogen Ingredients
        { data: 4 }, // Total Nitrogen in Product
        { data: 5 }, // Percentage of Nitrogen Ingredients
        { data: 6 }, // Product Category
      ],
    });
  }

  // Function to apply filters based on the current selections
  function applyFilters(minNitrogen = 0, maxNitrogen = 100) {
    const brand = document.getElementById('brandSelect').value;
    const category = document.getElementById('categorySelect').value;
    const productName = document
      .getElementById('productNamesearch')
      .value.toLowerCase();

    const rows = document.querySelectorAll('#NitrogenTable tbody tr');
    rows.forEach((row) => {
      const rowBrand = row.cells[0].innerText;
      const rowCategory = row.cells[6].innerText;
      const rowProductName = row.cells[1].innerText.toLowerCase();
      const rowNitrogen = parseFloat(row.cells[5].innerText);

      const brandMatch = brand ? rowBrand === brand : true;
      const categoryMatch = category ? rowCategory === category : true;
      const productNameMatch = productName
        ? rowProductName.includes(productName)
        : true;
      const nitrogenMatch =
        rowNitrogen >= minNitrogen && rowNitrogen <= maxNitrogen;

      row.style.display =
        brandMatch && categoryMatch && productNameMatch && nitrogenMatch
          ? ''
          : 'none';
    });
  }

  // Call getData when the page is loaded
  document.addEventListener('DOMContentLoaded', getData);

  // Buttons Apply Filters and Reset Filters
  document
    .getElementById('applyFilters')
    .addEventListener('click', function () {
      const nitrogenSliderValues = nitrogenSlider.noUiSlider.get();
      const minNitrogen = parseFloat(nitrogenSliderValues[0]);
      const maxNitrogen = parseFloat(nitrogenSliderValues[1]);

      applyFilters(minNitrogen, maxNitrogen);
    });

  document
    .getElementById('resetFilters')
    .addEventListener('click', function () {
      document.getElementById('brandSelect').selectedIndex = -1; // Reset brand selection
      document.getElementById('categorySelect').selectedIndex = -1; // Reset category selection
      document.getElementById('productNamesearch').value = ''; // Clear product name search
      nitrogenSlider.noUiSlider.set([0, 100]); // Reset slider

      const rows = document.querySelectorAll('#NitrogenTable tbody tr');
      rows.forEach((row) => (row.style.display = '')); // Show all rows
    });

  const nitrogenPercentage = parseFloat(
    document.getElementById('nitrogenPercentageslider').value
  );

  const rows = document.querySelectorAll('#NitrogenTable tbody tr');
  rows.forEach((row) => {
    const rowBrand = row.cells[0].innerText;
    const rowCategory = row.cells[6].innerText;
    const rowProductName = row.cells[1].innerText.toLowerCase();
    const rowNitrogen = parseFloat(row.cells[5].innerText);

    const brandMatch = brand ? rowBrand === brand : true;
    const categoryMatch = category ? rowCategory === category : true;
    const productNameMatch = productName
      ? rowProductName.includes(productName)
      : true;
    const nitrogenMatch = !isNaN(nitrogenPercentage)
      ? rowNitrogen >= nitrogenPercentage
      : true;

    row.style.display =
      brandMatch && categoryMatch && productNameMatch && nitrogenMatch
        ? ''
        : 'none';
  });
});

document.getElementById('resetFilters').addEventListener('click', function () {
  document.getElementById('brandSelect').selectedIndex = 0;
  document.getElementById('categorySelect').selectedIndex = 0;
  document.getElementById('productName').value = '';
  document.getElementById('nitrogenPercentage').value = '';

  const rows = document.querySelectorAll('#NitrogenTable tbody tr');
  rows.forEach((row) => (row.style.display = ''));
});

