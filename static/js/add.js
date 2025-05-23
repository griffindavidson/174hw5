const submitButton = document.getElementById('submit');

function addAddress() {
    const container = document.getElementById("addresses");

    const addressField = document.createElement("input");
    addressField.setAttribute("type", "text");
    addressField.setAttribute("name", "address");
    addressField.setAttribute("placeholder", "123 Park Way, Atlanta, Georgia, U.S.");

    const descriptionField = document.createElement("input");
    descriptionField.setAttribute("type", "text");
    descriptionField.setAttribute("name", "address");
    descriptionField.setAttribute("placeholder", "Description of Hub");

    container.appendChild(addressField);
    container.appendChild(descriptionField);
}

submitButton.addEventListener("click", () => {

    // grab all inputs into constants
    const name = document.getElementById('name').value;
    const services = document.getElementById('services').value;
    const hubs = Array.from(document.querySelectorAll('input[name="address"]'))
        .map(input => input.value)
        .filter(value => value.trim() !== '');
    const revenue = document.getElementById('revenue').value;
    const homepage = document.getElementById('homepage').value;
    const file = document.getElementById('logo').files[0];

    fileToBase64(file)
        .then(string => {
            const body = {
                row: {
                    Company: name,
                    Services: services,
                    Hubs: {
                        Hub: hubs
                    },
                    Revenue: revenue ? "$" + revenue : "",
                    HomePage: homepage,
                    Logo:  file ? file.name : ""
                },
                file: string
            }

             // create request and turn JS Object into JSON
            const request = new Request("/companies", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body),
            });

            // query flask and await response
            fetch(request)
                .then(response => response.json())
                .then(data => {
                    // do something with response
                    if (data.success) {
                        console.log(data.success);
                        showToast("success", data.success);
                    } else {
                        console.error(data.error);
                        showToast("error", data.error);
                    }
                })
                .catch(error => console.error("Error: ", error));
        })
        .catch(error => console.error("Error: ", error));    
});

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        if (!file) { 
            resolve("") // return empty string if no file present
            return;
        } 

        const reader = new FileReader();

        reader.onload = () => resolve(reader.result);  // On success, resolve with base64
        reader.onerror = () => reject(new Error("Failed to read file"));  // Reject if an error occurs
        reader.readAsDataURL(file);  // Start reading the file as base64
    });
}

function showToast(state, message) {
    const toast = document.createElement('div');
    toast.style.display = 'flex';
    toast.style.position = 'fixed';
    toast.style.bottom = '5px';
    toast.style.left = '5px';
    toast.style.width = 'fit-content';
    toast.style.height = 'fit-content';
    toast.style.color = 'white';
    toast.style.padding = '1rem';
    toast.style.borderRadius = '1rem';

    if (state === "success") {
        toast.innerText = "Company successfully added!";
        toast.style.backgroundColor = 'lime';
    } else {
        toast.innerText = "Error: " + message;
        toast.style.backgroundColor = 'red';
    }

    document.body.appendChild(toast);

    setTimeout(() => {
        document.body.removeChild(toast);
    }, 5000);
}
