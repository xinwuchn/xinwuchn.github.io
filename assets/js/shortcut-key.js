// Keep the platform shortcut in the tooltip so the navigation stays compact.
document.addEventListener("DOMContentLoaded", () => {
  const searchToggle = document.getElementById("search-toggle");
  if (searchToggle) {
    const shortcut = navigator.platform.toUpperCase().includes("MAC")
      ? "⌘ K"
      : "Ctrl K";
    searchToggle.title = `Search (${shortcut})`;
  }
});
