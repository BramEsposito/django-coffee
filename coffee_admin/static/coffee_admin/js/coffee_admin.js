/**
 * Coffee Admin JavaScript
 *
 * This file is loaded on every Django admin page.
 * Add your custom admin JavaScript functionality here.
 *
 * Features:
 * - Configurable keystroke listener
 *
 * Usage:
 * You can override the keystroke handler:
 *   window.CoffeeAdmin.onKeystrokeTriggered = function(event) {
 *     // Your custom logic here
 *   };
 */

(function() {
    'use strict';

    // Keystroke configuration
    var keystrokeConfig = {
        altKey: true,
        ctrlKey: false,
        shiftKey: false,
        key: 'd'  // The key to listen for (case-insensitive)
    };

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
        // Check if the configured keystroke combination matches
        var keyMatches = event.key.toLowerCase() === keystrokeConfig.key.toLowerCase();
        var altMatches = event.altKey === keystrokeConfig.altKey;
        var ctrlMatches = event.ctrlKey === keystrokeConfig.ctrlKey;
        var shiftMatches = event.shiftKey === keystrokeConfig.shiftKey;

        if (keyMatches && altMatches && ctrlMatches && shiftMatches) {
            event.preventDefault(); // Prevent default browser behavior
            onKeystrokeTriggered(event);
        }
    }

    /**
     * Handler for configured keystroke
     * @param {KeyboardEvent} event - The keyboard event
     */
    function onKeystrokeTriggered(event) {
        console.log('Configured keystroke triggered in Coffee Admin');
        // Add your custom keystroke functionality here
        // Example: Toggle a panel, show a dialog, etc.
    }

    // Expose public API if needed
    window.CoffeeAdmin = {
        init: initCoffeeAdmin,
        version: '0.1.0',
        // Expose keystroke handler for customization
        onKeystrokeTriggered: onKeystrokeTriggered
    };

})();
