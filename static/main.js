// static/main.js

document.addEventListener("DOMContentLoaded", function () {
    
    // 1. Fetch the data from your Django API View
    fetch('/api/resources/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Data loaded:", data); // Check your browser console for this!
            
            // 2. Map service types to your HTML IDs
            const grids = {
                "Compute": document.getElementById('compute-grid'),
                "Storage": document.getElementById('storage-grid'),
                "Database": document.getElementById('database-grid'),
                "Trending": document.getElementById('trending-grid') 
            };

            // 3. Loop through data and create HTML cards
            data.forEach(service => {
                const card = document.createElement('div');
                card.className = 'service-card'; // Changed class to match CSS better
                
                // Use icon from DB or default
                const iconUrl = service.icon_url || "https://img.icons8.com/color/96/amazon-web-services.png";

                card.innerHTML = `
                    <img src="${iconUrl}" alt="${service.name}" style="width:64px; height:64px; margin-bottom:10px;">
                    <div style="font-weight:bold; color:#003366;">${service.name}</div>
                    <span style="font-size:12px; color:#555; background:#eee; padding:2px 6px; border-radius:4px; margin-top:5px;">${service.status}</span>
                `;

                // 4. Inject into specific category
                if (grids[service.type]) {
                    grids[service.type].appendChild(card);
                }
                
                // 5. Also inject into Trending (Clone the card so it appears in both places)
                if (grids["Trending"]) {
                    grids["Trending"].appendChild(card.cloneNode(true));
                }
            });
        })
        .catch(error => console.error('Error loading resources:', error));
});

// --- Hero Slider Logic (Keep this) ---
let currentSlide = 0;
function moveHero(direction) {
    const track = document.getElementById('heroTrack');
    const slides = document.querySelectorAll('.hero-slide');
    const totalSlides = slides.length;
    if(totalSlides === 0) return;

    currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
    track.style.transform = `translateX(-${currentSlide * 100}%)`;
}