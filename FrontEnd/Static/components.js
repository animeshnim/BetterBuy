// Navigation Bar
function toggle_secondary_navbar(display) {
    if (display == 'show') {
        primary_navbar = document.querySelector('#primary-navbar');
        primary_navbar.classList.add('hidden');
        secondary_navbar = document.querySelector('#secondary-navbar');
        secondary_navbar.classList.add('flex');
        secondary_navbar.classList.remove('hidden');
    }

    else if (display == 'hide') {
        primary_navbar = document.querySelector('#primary-navbar');
        primary_navbar.classList.remove('hidden');
        secondary_navbar = document.querySelector('#secondary-navbar');
        secondary_navbar.classList.add('hidden');
    }
}

function menu_button_action() {
    menu_section = document.querySelector('#menu-section');
    menu_button = document.querySelector('#menu-button');
    cancel_button = document.querySelector('#cancel-button');
    secondary_navbar = document.querySelector('#secondary-navbar');
    main_content = document.querySelector('#main-content');
    footer = document.querySelector('#footer');

    menu_section.classList.remove('hidden');
    menu_button.classList.add('hidden');
    cancel_button.classList.remove('hidden');
    secondary_navbar.classList.add('hidden');
    main_content.classList.add('hidden');
    footer.classList.add('hidden');
}


function cancel_button_action() {
    menu_section = document.querySelector('#menu-section');
    menu_button = document.querySelector('#menu-button');
    cancel_button = document.querySelector('#cancel-button');
    secondary_navbar = document.querySelector('#secondary-navbar');
    main_content = document.querySelector('#main-content');
    footer = document.querySelector('#footer');

    menu_section.classList.add('hidden');
    menu_button.classList.remove('hidden');
    cancel_button.classList.add('hidden');
    secondary_navbar.classList.remove('hidden');
    main_content.classList.remove('hidden');
    footer.classList.remove('hidden');
}



// Modal Functionality (Open/Close Modal)
function open_modal_button_action(element_id) {
    let modal = document.querySelector(`#${element_id}`);
    modal.classList.add('flex');
    modal.classList.remove('hidden');
    modal.setAttribute("data-state", "opened");
}

function close_modal_button_action() {
    let modals = document.querySelectorAll('[data-state="opened"]');

    for (modal of modals) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        modal.setAttribute("data-state", "closed");
    }
}



// Add to Wishlist Modal
function set_value_of_product_slug(value) {
    input_tag = document.querySelector('#product-slug');
    input_tag.value = value;
}

function new_wishlist_button_action() {
    let new_wishlist_name_input = document.querySelector('#new-wishlist-name-input');
    let create_new_wishlist_button = document.querySelector('#new-wishlist-button');
    let add_to_new_wishlist_button = document.querySelector('#add-to-new-wishlist-button');

    new_wishlist_name_input.classList.remove('hidden')
    add_to_new_wishlist_button.classList.remove('hidden')
    create_new_wishlist_button.classList.add('hidden');
}

function add_to_new_wishlist_button_action() {
    let wishlist_id_inputs = document.querySelectorAll('.wishlist-id-input');
    let new_wishlist_name_input = document.querySelector('#new-wishlist-name-input');
    
    new_wishlist_name_input.required = true;
    for (wishlist_id_input of wishlist_id_inputs) {
        wishlist_id_input.removeAttribute('required');
    }
}

function add_to_selected_wishlist_action() {
    let new_wishlist_name_input = document.querySelector('#new-wishlist-name-input');
    let wishlist_id_inputs = document.querySelectorAll('.wishlist-id-input');
    
    new_wishlist_name_input.removeAttribute('required');
    for (wishlist_id_input of wishlist_id_inputs) {
        wishlist_id_input.required = true;
    }
}



// Add New Address Modal
function get_postal_code_details(element) {
    let pincode = element.value;
    console.log(pincode);

    if (pincode.length == 6) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                let data = this.response;
                let data_status = JSON.parse(data)[0]['Status'];
                let area_input = document.querySelector('#area-input');
                console.log(data_status);

                if (data_status == "Success") {
                    let all_areas = JSON.parse(data)[0]['PostOffice'];
                    
                    let city_input = document.querySelector('#city-input');
                    let district_input = document.querySelector('#district-input');
                    let state_input = document.querySelector('#state-input');

                    city_input.value = all_areas[0]['Block'];
                    district_input.value = all_areas[0]['District'];
                    state_input.value = all_areas[0]['State'];

                    for (area of all_areas) {
                        area_input.insertAdjacentHTML('beforeend', `<option value="${area.Name}">${area.Name}</option>`);
                    }
                }

                else if (data_status == "Error") {
                    area_input.innerHTML = '';
                }
            }
        };
        
        xhttp.open("GET", `https://api.postalpincode.in/pincode/${pincode}`, true);
        xhttp.send();
        console.log('awaiting response');
    }


    else {
        let area_input = document.querySelector('#area-input');
        area_input.innerHTML = '';
    }
}



// Edit Address
function set_value_of_address_unique_id(value) {
    input_tag = document.querySelector('#address-unique-id-input');
    input_tag.value = value;
}

function set_input_values(type, name, contact, house, street, landmark, pincode, city, district, state, selected) {
    let address_type_input = document.querySelector('#address-type-input');
    let name_input = document.querySelector('#name-input-e');
    let contact_no_input = document.querySelector('#contact-no-input-e');
    let house_no_input = document.querySelector('#house-no-input-e');
    let street_or_colony_input = document.querySelector('#street-or-colony-input-e');
    let landmark_input = document.querySelector('#landmark-input-e');
    let pincode_input = document.querySelector('#pincode-input-e');
    let city_input = document.querySelector('#city-input-e');
    let district_input = document.querySelector('#district-input-e');
    let state_input = document.querySelector('#state-input-e');
    let default_input = document.querySelector('#default-input-e');
    
    if (type == 'HOME') {
        let type_input = document.querySelector('#address-type-home');
        type_input.checked = true;
    }

    else if (type == 'WORK') {
        let type_input = document.querySelector('#address-type-work');
        type_input.checked = true;
    }

    if (selected == 'True') {
        default_input.checked = true;
    }

    name_input.value = name;
    contact_no_input.value = contact;
    house_no_input.value = house;
    street_or_colony_input.value = street;
    landmark_input.value = landmark;
    pincode_input.value = pincode;
    city_input.value = city;
    district_input.value = district;
    state_input.value = state;
}


function get_postal_code_details_edit_form(element) {
    let pincode = element.value;

    if (pincode.length == 6) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                let data = this.response;
                let data_status = JSON.parse(data)[0]['Status'];
                let area_input = document.querySelector('#area-input-e');

                if (data_status == "Success") {
                    let all_areas = JSON.parse(data)[0]['PostOffice'];
                    
                    let city_input = document.querySelector('#city-input-e');
                    let district_input = document.querySelector('#district-input-e');
                    let state_input = document.querySelector('#state-input-e');

                    city_input.value = all_areas[0]['Block'];
                    district_input.value = all_areas[0]['District'];
                    state_input.value = all_areas[0]['State'];

                    for (area of all_areas) {
                        area_input.insertAdjacentHTML('beforeend', `<option value="${area.Name}">${area.Name}</option>`);
                    }
                }

                else if (data_status == "Error") {
                    area_input.innerHTML = '';
                }
            }
        };
        
        xhttp.open("GET", `https://api.postalpincode.in/pincode/${pincode}`, true);
        xhttp.send();
        console.log('awaiting response');
    }


    else {
        let area_input = document.querySelector('#area-input-e');
        area_input.innerHTML = '';
    }
}


function prefill_area_details(pincode, area_name) {
    let prefill_pincode = pincode;
    let pincode_input = document.querySelector('#pincode-input-e');
    

    if (pincode_input.value == prefill_pincode) {
        if (pincode.length == 6) {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    let data = this.response;
                    let data_status = JSON.parse(data)[0]['Status'];
                    let area_input = document.querySelector('#area-input-e');
    
                    if (data_status == "Success") {
                        let all_areas = JSON.parse(data)[0]['PostOffice'];
                        
                        let city_input = document.querySelector('#city-input-e');
                        let district_input = document.querySelector('#district-input-e');
                        let state_input = document.querySelector('#state-input-e');
    
                        city_input.value = all_areas[0]['Block'];
                        district_input.value = all_areas[0]['District'];
                        state_input.value = all_areas[0]['State'];
    
                        for (area of all_areas) {
                            if (area_name == area.Name) {
                                area_input.insertAdjacentHTML('beforeend', `<option value="${area.Name}" selected>${area.Name}</option>`);
                            }

                            else {
                                area_input.insertAdjacentHTML('beforeend', `<option value="${area.Name}">${area.Name}</option>`);
                            }
                        }
                    }
    
                    else if (data_status == "Error") {
                        area_input.innerHTML = '';
                    }
                }
            };
            
            xhttp.open("GET", `https://api.postalpincode.in/pincode/${pincode}`, true);
            xhttp.send();
            console.log('awaiting response');
        }


        else {
            let area_input = document.querySelector('#area-input-e');
            area_input.innerHTML = '';
        }
    }

}