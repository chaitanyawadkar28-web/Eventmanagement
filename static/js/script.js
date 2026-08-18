// ==========================================
// EventEase Maharashtra - JavaScript
// ==========================================


// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("EventEase Maharashtra loaded successfully!");

    // Venue details page आहे का ते check करा
    if (typeof selectedVenue !== "undefined") {

        loadVenueDetails();

    }

});


// ==========================================
// VENUE DATA
// ==========================================

const venues = [

    // ======================================
    // SOLAPUR VENUE 1
    // ======================================

    {
        name: "Royal Palace Hall",
        district: "Solapur",

        events: [
            "Marriage",
            "Engagement",
            "Reception"
        ],

        budget: "₹1,00,000 - ₹2,00,000",
        guests: "500",
        phone: "9876543210",
        address: "Hotgi Road, Solapur",

        image: "royal_palace_hall.png"
    },


    // ======================================
    // SOLAPUR VENUE 2
    // ======================================

    {
        name: "Grand Celebration Hall",
        district: "Solapur",

        events: [
            "Marriage",
            "Birthday Party",
            "Engagement"
        ],

        budget: "₹2,00,000 - ₹5,00,000",
        guests: "800",
        phone: "9876501234",
        address: "Akkalkot Road, Solapur",

        image: "grand_celebration_hall.png"
    },


    // ======================================
    // SOLAPUR VENUE 3
    // ======================================

    {
        name: "Sahyadri Mangal Karyalay",
        district: "Solapur",

        events: [
            "Marriage",
            "Engagement",
            "Reception"
        ],

        budget: "₹1,00,000 - ₹2,00,000",
        guests: "600",
        phone: "9876534567",
        address: "Hotgi Road, Solapur",

        image: "sahyadri_hall.png"
    },


    // ======================================
    // SOLAPUR VENUE 4
    // ======================================

    {
        name: "Shree Ganesh Banquet Hall",
        district: "Solapur",

        events: [
            "Marriage",
            "Birthday Party",
            "Engagement"
        ],

        budget: "₹50,000 - ₹1,00,000",
        guests: "400",
        phone: "9876545678",
        address: "Vijapur Road, Solapur",

        image: "ganesh_banquet.png"
    },


    // ======================================
    // PUNE VENUE 1
    // ======================================

    {
        name: "Sunshine Party Hall",
        district: "Pune",

        events: [
            "Birthday Party",
            "Engagement",
            "Anniversary"
        ],

        budget: "₹50,000 - ₹1,00,000",
        guests: "300",
        phone: "9876512345",
        address: "Baner, Pune",

        image: "sunshine_party_hall.png"
    },


    // ======================================
    // PUNE VENUE 2
    // ======================================

    {
        name: "Grand Orchid Banquet",
        district: "Pune",

        events: [
            "Marriage",
            "Reception",
            "Corporate Event"
        ],

        budget: "₹2,00,000 - ₹5,00,000",
        guests: "1000",
        phone: "9876523456",
        address: "Wakad, Pune",

        image: "grand_orchid_banquet.png"
    }

];


// ==========================================
// SEARCH VENUE
// ==========================================

function searchVenue() {

    const district =
        document.getElementById("district").value;

    const eventType =
        document.getElementById("eventType").value;

    const budget =
        document.getElementById("budget").value;

    const guests =
        document.getElementById("guests").value;


    const message =
        document.getElementById("searchMessage");

    const venueContainer =
        document.getElementById("venueContainer");


    // Check fields

    if (
        district === "" ||
        eventType === "" ||
        budget === "" ||
        guests === ""
    ) {

        message.style.color = "red";

        message.innerText =
            "Please select District, Event Type, Budget and Number of Guests.";

        venueContainer.innerHTML = "";

        return;
    }


    // Filter venues

    const matchingVenues = venues.filter(function (venue) {

        return (
            venue.district === district &&
            venue.events.includes(eventType)
        );

    });


    // Show result

    message.style.color = "green";

    message.innerText =
        matchingVenues.length +
        " venue(s) found in " +
        district;


    venueContainer.innerHTML = "";


    // No result

    if (matchingVenues.length === 0) {

        venueContainer.innerHTML = `

            <div class="no-results">

                <h3>No venues found</h3>

                <p>
                    Try another event type or district.
                </p>

            </div>

        `;

        return;
    }


    // Create cards

    matchingVenues.forEach(function (venue) {

        const card =
            document.createElement("div");

        card.className = "venue-card";


        card.innerHTML = `

            <img
                src="/static/images/${venue.image}"
                class="venue-image"
                alt="${venue.name}"
            >


            <div class="venue-info">

                <h3>
                    ${venue.name}
                </h3>


                <p>
                    📍 ${venue.address}
                </p>


                <p>
                    🎉 Suitable for:
                    ${venue.events.join(", ")}
                </p>


                <p>
                    👥 Capacity:
                    ${venue.guests} Guests
                </p>


                <p class="price">
                    💰 ${venue.budget}
                </p>


                <p>
                    📞 ${venue.phone}
                </p>


                <div class="venue-buttons">

                    <button
                        class="btn details-btn"
                        onclick="viewVenue('${venue.name}')">

                        👁️ View Details

                    </button>


                    <button
                        class="btn contact-btn"
                        onclick="contactVenue('${venue.phone}')">

                        📞 Contact

                    </button>

                </div>

            </div>

        `;


        venueContainer.appendChild(card);

    });


    // Scroll to results

    const resultsSection =
        document.getElementById("venueResults");

    if (resultsSection) {

        resultsSection.scrollIntoView({
            behavior: "smooth"
        });

    }

}


// ==========================================
// VIEW VENUE
// ==========================================

function viewVenue(venueName) {

    window.location.href =
        "/venue/" +
        encodeURIComponent(venueName);

}


// ==========================================
// LOAD VENUE DETAILS
// ==========================================

function loadVenueDetails() {

    const venue = venues.find(function (item) {

        return item.name === selectedVenue;

    });


    // Venue not found

    if (!venue) {

        console.log("Venue not found");

        return;

    }


    // ======================================
    // VENUE NAME
    // ======================================

    const nameElement =
        document.getElementById("venueName");

    if (nameElement) {

        nameElement.innerText =
            venue.name;

    }


    // ======================================
    // VENUE IMAGE
    // ======================================

    const imageElement =
        document.getElementById("venueImage");

    if (imageElement) {

        imageElement.src =
            "/static/images/" + venue.image;

        imageElement.alt =
            venue.name;

    }


    // ======================================
    // ADDRESS
    // ======================================

    const addressElement =
        document.getElementById("venueAddress");

    if (addressElement) {

        addressElement.innerText =
            "📍 " + venue.address;

    }


    // ======================================
    // EVENTS
    // ======================================

    const eventsElement =
        document.getElementById("venueEvents");

    if (eventsElement) {

        eventsElement.innerText =
            "🎉 Suitable for: " +
            venue.events.join(", ");

    }


    // ======================================
    // GUEST CAPACITY
    // ======================================

    const guestsElement =
        document.getElementById("venueGuests");

    if (guestsElement) {

        guestsElement.innerText =
            "👥 Capacity: " +
            venue.guests +
            " Guests";

    }


    // ======================================
    // BUDGET
    // ======================================

    const budgetElement =
        document.getElementById("venueBudget");

    if (budgetElement) {

        budgetElement.innerText =
            "💰 Budget: " +
            venue.budget;

    }


    // ======================================
    // PHONE
    // ======================================

    const phoneElement =
        document.getElementById("venuePhone");

    if (phoneElement) {

        phoneElement.innerText =
            "📞 " +
            venue.phone;

    }


    // ======================================
    // CONTACT BUTTON
    // ======================================

    const contactButton =
        document.getElementById("contactButton");

    if (contactButton) {

        contactButton.onclick = function () {

            contactVenue(venue.phone);

        };

    }

}


// ==========================================
// CONTACT VENUE
// ==========================================

function contactVenue(phone) {

    alert(

        "📞 Contact Venue\n\n" +

        "Phone Number: " +
        phone

    );

}