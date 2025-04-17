function addAddress() {
    const container = document.getElementById("addresses");
    const field = document.createElement("input");
    
    field.setAttribute("type", "text");
    field.setAttribute("name", "address");
    field.setAttribute("placeholder", "123 Park Way, Atlanta, Georgia, U.S.");

    container.appendChild(field);
  }