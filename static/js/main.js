document.addEventListener('DOMContentLoaded', () => {
    // --- THEME TOGGLE LOGIC ---
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const htmlElement = document.documentElement;

    // Load initial theme from localStorage or system preferences
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
        updateThemeToggleIcon(savedTheme);
    } else {
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const defaultTheme = systemPrefersDark ? 'dark' : 'light';
        htmlElement.setAttribute('data-theme', defaultTheme);
        updateThemeToggleIcon(defaultTheme);
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeToggleIcon(newTheme);
        });
    }

    function updateThemeToggleIcon(theme) {
        if (!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
            themeToggleBtn.setAttribute('title', 'Switch to Light Mode');
        } else {
            icon.className = 'fas fa-moon';
            themeToggleBtn.setAttribute('title', 'Switch to Dark Mode');
        }
    }

    // --- PASSWORD VISIBILITY TOGGLE ---
    const togglePasswordButtons = document.querySelectorAll('.toggle-password-btn');
    togglePasswordButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const inputId = btn.getAttribute('data-target');
            const inputField = document.getElementById(inputId);
            const icon = btn.querySelector('i');

            if (inputField) {
                if (inputField.type === 'password') {
                    inputField.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    inputField.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });

    // --- ADMIN RETRAIN PROGRESS POLLING ---
    const retrainStatusBox = document.getElementById('retrain-status-box');
    const retrainSpinner = document.getElementById('retrain-spinner');
    const retrainMsgText = document.getElementById('retrain-message-text');
    const modelRetrainForm = document.getElementById('model-retrain-form');

    if (retrainStatusBox) {
        // Check if training was already running on load
        checkRetrainStatus();
    }

    if (modelRetrainForm) {
        modelRetrainForm.addEventListener('submit', () => {
            // Give a short delay then check status
            setTimeout(checkRetrainStatus, 1000);
        });
    }

    let pollInterval = null;

    function checkRetrainStatus() {
        fetch('/admin/retrain_status')
            .then(response => response.json())
            .then(data => {
                if (data.is_retraining) {
                    if (retrainStatusBox) {
                        retrainStatusBox.classList.remove('d-none');
                        retrainSpinner.classList.remove('d-none');
                        retrainMsgText.textContent = data.message || "Model training in progress...";
                    }
                    
                    // Poll again in 3 seconds
                    if (!pollInterval) {
                        pollInterval = setInterval(checkRetrainStatus, 3000);
                    }
                } else {
                    if (pollInterval) {
                        clearInterval(pollInterval);
                        pollInterval = null;
                        // Reload page to refresh metrics and status
                        window.location.reload();
                    }
                    if (retrainStatusBox) {
                        retrainMsgText.textContent = data.message || "Model is ready.";
                        retrainSpinner.classList.add('d-none');
                    }
                }
            })
            .catch(err => {
                console.error("Error fetching retraining status:", err);
            });
    }

    // --- ACTION CONFIRMATION PROMPTS ---
    const confirmActions = document.querySelectorAll('.confirm-action');
    confirmActions.forEach(element => {
        element.addEventListener('click', (e) => {
            const message = element.getAttribute('data-confirm-message') || "Are you sure you want to perform this action?";
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // --- FORM AUTO-VALIDATOR SPINNERS ---
    const predictForm = document.getElementById('job-predict-form');
    if (predictForm) {
        predictForm.addEventListener('submit', (e) => {
            const titleInput = document.getElementById('title');
            const descInput = document.getElementById('description');
            
            if (titleInput.value.trim() === '' || descInput.value.trim() === '') {
                e.preventDefault();
                alert("Please fill in both Job Title and Job Description fields.");
                return;
            }

            const submitBtn = predictForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing Job Posting...';
        });
    }
});
