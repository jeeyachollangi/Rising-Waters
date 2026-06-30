document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // Form Input Validation & Verification
    // ----------------------------------------------------
    const predictForm = document.getElementById('predict-form');
    if (predictForm) {
        const cloudInput = document.getElementById('cloud_cover');
        const annualInput = document.getElementById('annual_rainfall');
        const janFebInput = document.getElementById('jan_feb');
        const marMayInput = document.getElementById('mar_may');
        const junSepInput = document.getElementById('jun_sep');
        
        predictForm.addEventListener('submit', (e) => {
            let isValid = true;
            let errors = [];

            // Parse values
            const cloudVal = parseFloat(cloudInput.value);
            const annualVal = parseFloat(annualInput.value);
            const janFebVal = parseFloat(janFebInput.value);
            const marMayVal = parseFloat(marMayInput.value);
            const junSepVal = parseFloat(junSepInput.value);

            // Validate Cloud Cover
            if (isNaN(cloudVal) || cloudVal < 0 || cloudVal > 100) {
                isValid = false;
                errors.push("Cloud Cover must be a percentage between 0% and 100%.");
                cloudInput.style.borderColor = "var(--danger)";
            } else {
                cloudInput.style.borderColor = "";
            }

            // Validate Annual Rainfall
            if (isNaN(annualVal) || annualVal < 0 || annualVal > 20000) {
                isValid = false;
                errors.push("Annual Rainfall must be a positive number between 0 and 20,000 mm.");
                annualInput.style.borderColor = "var(--danger)";
            } else {
                annualInput.style.borderColor = "";
            }

            // Validate negative checks
            if (isNaN(janFebVal) || janFebVal < 0) {
                isValid = false;
                errors.push("Jan-Feb Rainfall cannot be negative.");
                janFebInput.style.borderColor = "var(--danger)";
            } else {
                janFebInput.style.borderColor = "";
            }

            if (isNaN(marMayVal) || marMayVal < 0) {
                isValid = false;
                errors.push("March-May Rainfall cannot be negative.");
                marMayInput.style.borderColor = "var(--danger)";
            } else {
                marMayInput.style.borderColor = "";
            }

            if (isNaN(junSepVal) || junSepVal < 0) {
                isValid = false;
                errors.push("June-September Rainfall cannot be negative.");
                junSepInput.style.borderColor = "var(--danger)";
            } else {
                junSepInput.style.borderColor = "";
            }

            // Validate logical sum
            if (isValid && (janFebVal + marMayVal + junSepVal) > annualVal) {
                isValid = false;
                errors.push("Sum of seasonal rainfall (Jan-Feb, March-May, June-September) cannot exceed the total Annual Rainfall.");
                janFebInput.style.borderColor = "var(--danger)";
                marMayInput.style.borderColor = "var(--danger)";
                junSepInput.style.borderColor = "var(--danger)";
            }

            // Prevent submit if invalid, show premium dynamic error alert
            if (!isValid) {
                e.preventDefault();
                
                // Check if alert element already exists
                let alertBox = document.getElementById('alert-error');
                if (!alertBox) {
                    alertBox = document.createElement('div');
                    alertBox.id = 'alert-error';
                    alertBox.className = 'alert-error';
                    // Insert before form fields
                    predictForm.parentNode.insertBefore(alertBox, predictForm);
                }
                
                alertBox.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> <span>${errors.join(" | ")}</span>`;
                alertBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
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
