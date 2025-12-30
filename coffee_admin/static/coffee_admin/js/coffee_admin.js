/**
 * Coffee Admin JavaScript
 *
 * This file is loaded on every Django admin page.
 * Add your custom admin JavaScript functionality here.
 */

(function() {
    'use strict';

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Coffee Admin JavaScript loaded');

        // Add your custom initialization code here
        initCoffeeAdmin();
    });

    /**
     * Initialize Coffee Admin functionality
     */
    function initCoffeeAdmin() {
        // Stub function - implement your custom logic here
        // Example: Custom admin UI enhancements, event handlers, etc.
    }

    // Expose public API if needed
    window.CoffeeAdmin = {
        init: initCoffeeAdmin,
        version: '0.1.0'
    };

})();
