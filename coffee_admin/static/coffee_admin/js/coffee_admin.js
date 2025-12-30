/**
 * Coffee Admin JavaScript
 *
 * This file is loaded on every Django admin page.
 * Add your custom admin JavaScript functionality here.
 *
 * Features:
 * - Alt+D keystroke listener (customizable via window.CoffeeAdmin.onAltDPressed)
 *
 * Usage:
 * You can override the Alt+D handler:
 *   window.CoffeeAdmin.onAltDPressed = function(event) {
 *     // Your custom logic here
 *   };
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
        // Set up keystroke listeners
        setupKeystrokeListeners();
    }

    /**
     * Set up keyboard event listeners
     */
    function setupKeystrokeListeners() {
        document.addEventListener('keydown', handleKeystroke);
    }

    /**
     * Handle keyboard events
     * @param {KeyboardEvent} event - The keyboard event
     */
    function handleKeystroke(event) {
        // Check for Alt+D combination
        if (event.altKey && (event.key === 'd' || event.key === 'D')) {
            event.preventDefault(); // Prevent default browser behavior
            onAltDPressed(event);
        }
    }

    /**
     * Handler for Alt+D keystroke
     * @param {KeyboardEvent} event - The keyboard event
     */
    function onAltDPressed(event) {
        console.log('Alt+D pressed in Coffee Admin');
        // Add your custom Alt+D functionality here
        // Example: Toggle a panel, show a dialog, etc.
    }

    // Expose public API if needed
    window.CoffeeAdmin = {
        init: initCoffeeAdmin,
        version: '0.1.0',
        // Expose keystroke handler for customization
        onAltDPressed: onAltDPressed
    };

})();
