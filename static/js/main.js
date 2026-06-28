document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // Form Input Validation & Verification
    // ----------------------------------------------------
    const predictForm = document.getElementById('predict-form');
    if (predictForm) {
        const annualInput = document.getElementById('annual_rainfall');
        const seasonalInput = document.getElementById('seasonal_rainfall');
        const cloudInput = document.getElementById('cloud_visibility');
        const metInput = document.getElementById('meteorological_parameters');
        
        predictForm.addEventListener('submit', (e) => {
            let isValid = true;
            let errorMessage = "";

            // Parse values
            const annualVal = parseFloat(annualInput.value);
            const seasonalVal = parseFloat(seasonalInput.value);
            const cloudVal = parseFloat(cloudInput.value);
            const metVal = parseFloat(metInput.value);

            // Validate Annual Rainfall
            if (isNaN(annualVal) || annualVal < 0 || annualVal > 15000) {
                isValid = false;
                errorMessage += "• Annual Rainfall must be a positive number between 0 and 15,000 mm.\n";
                annualInput.classList.add('is-invalid');
            } else {
                annualInput.classList.remove('is-invalid');
            }

            // Validate Seasonal Rainfall
            if (isNaN(seasonalVal) || seasonalVal < 0 || seasonalVal > 10000) {
                isValid = false;
                errorMessage += "• Seasonal Rainfall must be a positive number between 0 and 10,000 mm.\n";
                seasonalInput.classList.add('is-invalid');
            } else if (seasonalVal > annualVal) {
                isValid = false;
                errorMessage += "• Seasonal Rainfall cannot be greater than Annual Rainfall.\n";
                seasonalInput.classList.add('is-invalid');
            } else {
                seasonalInput.classList.remove('is-invalid');
            }

            // Validate Cloud Visibility
            if (isNaN(cloudVal) || cloudVal < 0 || cloudVal > 100) {
                isValid = false;
                errorMessage += "• Cloud Visibility must be a percentage value between 0% and 100%.\n";
                cloudInput.classList.add('is-invalid');
            } else {
                cloudInput.classList.remove('is-invalid');
            }

            // Validate Meteorological Parameters
            if (isNaN(metVal) || metVal < 0 || metVal > 100) {
                isValid = false;
                errorMessage += "• Meteorological Index must be a scale value between 0 and 100.\n";
                metInput.classList.add('is-invalid');
            } else {
                metInput.classList.remove('is-invalid');
            }

            // Prevent submit if invalid
            if (!isValid) {
                e.preventDefault();
                alert("Please correct the following errors:\n\n" + errorMessage);
            } else {
                e.preventDefault(); // Prevent instant submit
                
                // Show the beautiful loading screen overlay
                const loadingOverlay = document.getElementById('loading-overlay');
                if (loadingOverlay) {
                    loadingOverlay.style.display = 'flex';
                }
                
                // Trigger form submission after 1.5 seconds to let the user see the analysis sequence
                setTimeout(() => {
                    predictForm.submit();
                }, 1500);
            }
        });
    }

    // Add active class to navigation links based on current path
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Add subtle visual feedback when buttons are clicked
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mousedown', () => {
            btn.style.transform = 'scale(0.97)';
        });
        btn.addEventListener('mouseup', () => {
            btn.style.transform = '';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });
});
