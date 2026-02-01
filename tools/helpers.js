// Helper functions and utilities

/**
 * Format a date string
 * @param {Date} date - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid, false otherwise
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Export functions if using modules
// export { formatDate, validateEmail };
