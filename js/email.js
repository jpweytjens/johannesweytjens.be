// The home page's email address, kept in two halves on its button so that
// no address sits in the page for a harvester to find. A click joins them
// into a mail link in the button's place; without this script the button
// stays hidden and the page spells the address out in words instead.
for (const button of document.querySelectorAll("button.icon-email")) {
  button.hidden = false;

  button.addEventListener("click", () => {
    const address = `${button.dataset.user}@${button.dataset.domain}`;

    const link = document.createElement("a");
    link.className = "icon-email revealed";
    link.href = `mailto:${address}`;
    link.append(button.querySelector("svg"));
    const label = document.createElement("span");
    label.textContent = address;
    link.append(label);

    button.replaceWith(link);
    link.focus();
  });
}
