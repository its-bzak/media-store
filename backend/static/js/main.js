console.log("This is JS from your about page");

// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", () => {
  const filterSelect = document.getElementById("filterSelect");
  const inStockCheckbox = document.getElementById("inStockOnly");
  const productCards = document.querySelectorAll(".product-card");

  if (!filterSelect || productCards.length === 0) {
    console.log("No product filtering elements found — likely not on the shop page.");
    return;
  }

  console.log("Product filtering enabled.");

  function filterProducts() {
    const selectedType = filterSelect.value.toLowerCase();
    const showInStockOnly = inStockCheckbox.checked;

    productCards.forEach(card => {
      const itemType = card.getAttribute("data-type").toLowerCase();
      const inStock = !card.querySelector(".buy-button").disabled;

      const matchesType = selectedType === "all items" || itemType === selectedType;
      const matchesStock = !showInStockOnly || inStock;

      // Show or hide the item based on filter
      card.style.display = (matchesType && matchesStock) ? "block" : "none";
    });
  }

  // Run filtering when selected option by user
  filterSelect.addEventListener("change", filterProducts);
  inStockCheckbox.addEventListener("change", filterProducts);

  // Run each page load
  filterProducts();
});
