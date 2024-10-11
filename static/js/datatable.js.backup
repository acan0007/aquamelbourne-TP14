let originalData = []; // Store the original data
let filteredData = []; // Store the filtered data

// Load Data and Populate Filters
async function getData() {
  // Load the Excel file
  const response = await fetch('/static/data.xlsx');
  const arrayBuffer = await response.arrayBuffer();

  // Use XLSX to parse the file
  const workbook = XLSX.read(arrayBuffer, { type: 'array' });
  const firstSheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[firstSheetName];

  // Convert the sheet to JSON
  originalData = XLSX.utils.sheet_to_json(worksheet, { header: 1 }); // Update the global `originalData`

  // Clear the tbody
  let tableBody = document.getElementById('tbody');
  tableBody.innerHTML = '';

  // Populate filters and initial table
  populateFilters(originalData);
  filteredData = originalData.slice(1); // Start with all data (excluding headers)
  populateTable(filteredData);

  // Initialize DataTables
  // $('#NitrogenTable').DataTable({
  //   data: filteredData, // Use filtered data for DataTable
  //   columns: [
  //     { data: 0 }, // Brand
  //     { data: 1 }, // Product Name
  //     { data: 2 }, // Ingredients containing Nitrogen
  //     { data: 3 }, // Number of Nitrogen Ingredients
  //     { data: 4 }, // Total Nitrogen in Product
  //     { data: 5 }, // Percentage of Nitrogen Ingredients
  //     { data: 6 }, // Product Category
  //   ],
  // });
}

// Populate Filters (Brand, Category, and Slider)
function populateFilters(data) {
  const brands = new Set();
  const categories = new Set();
  let minPercentage = Infinity;
  let maxPercentage = -Infinity;

  data.slice(1).forEach((row) => {
    if (row[0]) brands.add(row[0]); 
    if (row[6]) categories.add(row[6]); 
    if (row[5]) {
      const percentage = parseFloat(row[5]);
      if (!isNaN(percentage)) {
        minPercentage = Math.min(minPercentage, percentage);
        maxPercentage = Math.max(maxPercentage, percentage);
      }
    }
  });

  // Populate Brand filter
  const brandSelect = document.getElementById('brandSelect');
  brandSelect.innerHTML = ''; // Clear previous options
  brands.forEach((brand) => {
    const option = document.createElement('option');
    option.value = brand;
    option.textContent = brand;
    brandSelect.appendChild(option);
  });

  // Populate Category filter
  const categorySelect = document.getElementById('categorySelect');
  categorySelect.innerHTML = ''; // Clear previous options
  categories.forEach((category) => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
  });

  // Initialize Nitrogen Percentage Slider
  const nitrogenSlider = document.getElementById('nitrogenSlider');
  nitrogenSlider.noUiSlider?.destroy(); // Reset the slider if it already exists
  noUiSlider.create(nitrogenSlider, {
    start: [minPercentage, maxPercentage],
    connect: true,
    range: {
      min: minPercentage,
      max: maxPercentage,
    },
    tooltips: [true, true],
  });
}

// Apply Filters and Update filteredData
function applyFilters() {
  const brand = document.getElementById('brandSelect').value;
  const category = document.getElementById('categorySelect').value;
  const productName = document
    .getElementById('productNamesearch')
    .value.toLowerCase();
  const nitrogenSliderValues = document
    .getElementById('nitrogenSlider')
    .noUiSlider.get();
  const minNitrogen = parseFloat(nitrogenSliderValues[0]);
  const maxNitrogen = parseFloat(nitrogenSliderValues[1]);

  // Filter data based on selected filters
  filteredData = originalData.slice(1).filter((row) => {
    const rowBrand = row[0];
    const rowCategory = row[6];
    const rowProductName = row[1]?.toLowerCase();
    const rowNitrogen = parseFloat(row[5]);

    const brandMatch = brand ? rowBrand === brand : true;
    const categoryMatch = category ? rowCategory === category : true;
    const productNameMatch = productName
      ? rowProductName?.includes(productName)
      : true;
    const nitrogenMatch =
      !isNaN(rowNitrogen) &&
      rowNitrogen >= minNitrogen &&
      rowNitrogen <= maxNitrogen;

    return brandMatch && categoryMatch && productNameMatch && nitrogenMatch;
  });

  // Update the table with filtered data
  populateTable(filteredData);
}

// Populate the Table
function populateTable(data) {
  const tableBody = document.getElementById('tbody');
  tableBody.innerHTML = ''; // Clear previous rows

  data.forEach((row) => {
    const tableRow = `
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
    tableBody.innerHTML += tableRow; // Append new rows
  });
}

// Function to update summary statistics
function updateSummaryStatistics(data) {
  // Total number of products
  const totalProducts = data.length;

  // Variables for calculations
  let totalNitrogenIngredients = 0;
  let totalNitrogen = 0;
  let nitrogenPercentages = [];
  let nitrogenTotals = [];

  data.forEach((row) => {
    const nitrogenCount = parseInt(row[3], 10);
    const nitrogenPercentage = parseFloat(row[5]);
    const nitrogenTotal = parseFloat(row[4]);

    if (!isNaN(nitrogenCount)) {
      totalNitrogenIngredients += nitrogenCount;
    }

    if (!isNaN(nitrogenPercentage)) {
      nitrogenPercentages.push(nitrogenPercentage);
    }

    if (!isNaN(nitrogenTotal)) {
      totalNitrogen += nitrogenTotal;
      nitrogenTotals.push(nitrogenTotal);
    }
  });

  // Calculate the average percentage of nitrogen ingredients
  const averageNitrogenPercentage =
    nitrogenPercentages.reduce((sum, val) => sum + val, 0) /
    nitrogenPercentages.length;

  // Calculate the median percentage of nitrogen ingredients
  nitrogenPercentages.sort((a, b) => a - b);
  const medianNitrogenPercentage =
    nitrogenPercentages.length % 2 === 0
      ? (nitrogenPercentages[nitrogenPercentages.length / 2 - 1] +
          nitrogenPercentages[nitrogenPercentages.length / 2]) /
        2
      : nitrogenPercentages[Math.floor(nitrogenPercentages.length / 2)];

  // Calculate the max and min percentage of nitrogen ingredients
  const maxNitrogenPercentage = Math.max(...nitrogenPercentages);
  const minNitrogenPercentage = Math.min(...nitrogenPercentages);

  // Calculate the average total nitrogen per product
  const averageNitrogenPerProduct =
    nitrogenTotals.reduce((sum, val) => sum + val, 0) / nitrogenTotals.length;

  // Update the HTML with calculated values
  document.getElementById('totalProducts').textContent = totalProducts;
  document.getElementById('avgNitrogenPercentage').textContent = isNaN(
    averageNitrogenPercentage
  )
    ? '0'
    : averageNitrogenPercentage.toFixed(2);
  document.getElementById('totalNitrogenIngredients').textContent =
    totalNitrogenIngredients;
  document.getElementById('medianNitrogenPercentage').textContent = isNaN(
    medianNitrogenPercentage
  )
    ? '0'
    : medianNitrogenPercentage.toFixed(1);
  document.getElementById('maxNitrogenPercentage').textContent = isNaN(
    maxNitrogenPercentage
  )
    ? '0'
    : maxNitrogenPercentage.toFixed(1);
  document.getElementById('minNitrogenPercentage').textContent = isNaN(
    minNitrogenPercentage
  )
    ? '0'
    : minNitrogenPercentage.toFixed(1);
  document.getElementById('totalNitrogen').textContent = isNaN(totalNitrogen)
    ? '0'
    : totalNitrogen.toFixed(2);
  document.getElementById('avgNitrogenPerProduct').textContent = isNaN(
    averageNitrogenPerProduct
  )
    ? '0'
    : averageNitrogenPerProduct.toFixed(2);
}

// Call this function after filters are applied or when data is loaded
applyFilters = () => {
  const brand = document.getElementById('brandSelect').value;
  const category = document.getElementById('categorySelect').value;
  const productName = document
    .getElementById('productNamesearch')
    .value.toLowerCase();
  const nitrogenSliderValues = document
    .getElementById('nitrogenSlider')
    .noUiSlider.get();
  const minNitrogen = parseFloat(nitrogenSliderValues[0]);
  const maxNitrogen = parseFloat(nitrogenSliderValues[1]);

  // Filter data based on selected filters
  filteredData = originalData.slice(1).filter((row) => {
    const rowBrand = row[0];
    const rowCategory = row[6];
    const rowProductName = row[1]?.toLowerCase();
    const rowNitrogen = parseFloat(row[5]);

    const brandMatch = brand ? rowBrand === brand : true;
    const categoryMatch = category ? rowCategory === category : true;
    const productNameMatch = productName
      ? rowProductName?.includes(productName)
      : true;
    const nitrogenMatch =
      !isNaN(rowNitrogen) &&
      rowNitrogen >= minNitrogen &&
      rowNitrogen <= maxNitrogen;

    return brandMatch && categoryMatch && productNameMatch && nitrogenMatch;
  });

  // Update the table with filtered data
  populateTable(filteredData);

  // Update the summary statistics with the filtered data
  updateSummaryStatistics(filteredData);
};

// Also call updateSummaryStatistics when the data is initially loaded
document.addEventListener('DOMContentLoaded', () => {
  getData().then(() => {
    updateSummaryStatistics(filteredData);
  });
});

// Function to create the first bar chart (Nitrogen Ingredients in Products)
function createBarChart1(filteredData) {
  const ctx1 = document.getElementById('barChart1').getContext('2d');

  // Sort data based on nitrogen percentages in ascending order
  const sortedData = filteredData.sort(
    (a, b) => parseFloat(a[5]) - parseFloat(b[5])
  );

  const productNames = sortedData.map((row) => row[1]); // Assuming product name is in column 1
  const nitrogenPercentages = sortedData.map((row) => parseFloat(row[5])); // Nitrogen percentage in column 5

  new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: productNames,
      datasets: [
        {
          label: 'Percentage of Nitrogen Ingredients',
          data: nitrogenPercentages,
          backgroundColor: '#7464a1',
          borderColor: '#7464a1',
          borderWidth: 1,
        },
      ],
    },
    options: {
      indexAxis: 'y',
      scales: {
        x: {
          title: {
            display: true,
            text: 'Percentage of Nitrogen Ingredients',
          },
          grid: {
            display: false,
          },
        },
        y: {
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
      responsive: true,
    },
  });
}

// Function to create the second bar chart (Distribution of Products by Brand)
function createBarChart2(filteredData) {
  const ctx2 = document.getElementById('barChart2').getContext('2d');
  const brandCounts = {};

  // Counting the products by brand (assuming brand is in column 0)
  filteredData.forEach((row) => {
    const brand = row[0];
    if (brandCounts[brand]) {
      brandCounts[brand]++;
    } else {
      brandCounts[brand] = 1;
    }
  });

  // Extract brands and counts
  const brands = Object.keys(brandCounts);
  const counts = Object.values(brandCounts);

  // Combine brands and counts for sorting
  const combined = brands.map((brand, index) => {
    return { brand, count: counts[index] };
  });

  // Sort by count in ascending order
  combined.sort((a, b) => a.count - b.count);

  // Extract sorted brands and counts
  const sortedBrands = combined.map((item) => item.brand);
  const sortedCounts = combined.map((item) => item.count);

  // Create the bar chart
  new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: sortedBrands,
      datasets: [
        {
          label: 'Distribution of Products by Brand',
          data: sortedCounts,
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#4BC0C0',
            '#9966FF',
            '#FF9F40',
          ],
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          grid: {
            display: false,
          },
          title: {
            display: false,
          },
        },
        x: {
          grid: {
            display: false,
          },
          title: {
            display: true,
            text: 'Brands',
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  });
}

// Function to create the line chart (Nitrogen Ingredients vs Number of Nitrogen Ingredients)
function createLineChart(filteredData) {
  const ctx3 = document.getElementById('lineChart').getContext('2d');

  // Sort the data based on nitrogen percentages in ascending order
  filteredData.sort((a, b) => parseFloat(a[5]) - parseFloat(b[5]));

  const nitrogenPercentages = filteredData.map((row) => parseFloat(row[5])); 
  const nitrogenIngredients = filteredData.map((row) => parseInt(row[3], 10)); 

  // Determine the maximum nitrogen percentage
  const maxNitrogenPercentage = Math.max(...nitrogenPercentages);

  new Chart(ctx3, {
    type: 'line',
    data: {
      labels: nitrogenPercentages,
      datasets: [
        {
          label: 'Number of Ingredients Containing Nitrogen',
          data: nitrogenIngredients,
          fill: false,
          borderColor: '#7464a1',
          backgroundColor: '#aba2c6',
          borderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7,
        },
      ],
    },
    options: {
      scales: {
        x: {
          type: 'linear',
          title: {
            display: true,
            text: 'Percentage of Nitrogen Ingredients in the Product',
          },
          grid: {
            display: false,
          },
          ticks: {
            callback: function (value) {
              return value.toFixed(0);
            },
          },
          min: 0, // Set the minimum value to 0
          max: maxNitrogenPercentage + 5, 
        },
        y: {
          title: {
            display: true,
            text: 'Number of Ingredients Containing Nitrogen',
          },
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
      responsive: true,
    },
  });
}

// Call these functions after filters are applied or when data is loaded
document.addEventListener('DOMContentLoaded', () => {
  getData().then(() => {
    // Assuming `filteredData` has been populated in getData or applyFilters
    createBarChart1(filteredData);
    createBarChart2(filteredData);
    createLineChart(filteredData);
  });
});

// Reset Filters
function resetFilters() {
  // Reset filter values
  document.getElementById('brandSelect').selectedIndex = -1;
  document.getElementById('categorySelect').selectedIndex = -1;
  document.getElementById('productNamesearch').value = '';
 
  const nitrogenSlider = document.getElementById('nitrogenSlider');
  const sliderRange = nitrogenSlider.noUiSlider.options.range; // Get initial slider range
  nitrogenSlider.noUiSlider.set([sliderRange.min, sliderRange.max]); // Reset slider to initial range

  // Reset filteredData to original data
  filteredData = originalData.slice(1);

  // Update the table with the original data
  populateTable(filteredData);
}

// Event Listeners
document.getElementById('applyFilters').addEventListener('click', applyFilters);
document.getElementById('resetFilters').addEventListener('click', resetFilters);

// Call getData when the page is loaded
document.addEventListener('DOMContentLoaded', getData);
