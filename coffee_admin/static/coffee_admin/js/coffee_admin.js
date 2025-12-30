/**
 * Coffee Admin JavaScript
 *
 * This file is loaded on every Django admin page.
 * Add your custom admin JavaScript functionality here.
 *
 * Features:
 * - Configurable keystroke listener (default: Alt+D)
 * - Spotlight/Alfred-style launcher UI
 * - Real-time search of Django admin URLs
 * - Debounced API requests (300ms delay)
 * - Automatic navigation to selected results
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

    // Launcher state
    var launcherElement = null;
    var launcherInput = null;
    var isLauncherVisible = false;
    var searchDebounceTimer = null;
    var currentSearchRequest = null;

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
        // Create launcher UI
        createLauncher();
        // Set up keystroke listeners
        setupKeystrokeListeners();
    }

    /**
     * Create the launcher UI element
     */
    function createLauncher() {
        var backdrop = document.createElement('div');
        backdrop.className = 'coffee-launcher-backdrop';
        backdrop.innerHTML = `
            <div class="coffee-launcher">
                <div class="coffee-launcher-input-container">
                    <div class="coffee-launcher-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"></circle>
                            <path d="m21 21-4.35-4.35"></path>
                        </svg>
                    </div>
                    <input
                        type="text"
                        class="coffee-launcher-input"
                        placeholder="Type a command..."
                        autocomplete="off"
                        spellcheck="false"
                    />
                </div>
                <div class="coffee-launcher-results">
                    <div class="coffee-launcher-empty">
                        Start typing to search...
                    </div>
                </div>
                <div class="coffee-launcher-footer">
                    <div class="coffee-launcher-hint">
                        <span><kbd class="coffee-launcher-kbd">↵</kbd> to select</span>
                        <span><kbd class="coffee-launcher-kbd">↑</kbd><kbd class="coffee-launcher-kbd">↓</kbd> to navigate</span>
                    </div>
                    <div class="coffee-launcher-hint">
                        <span><kbd class="coffee-launcher-kbd">esc</kbd> to close</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(backdrop);
        launcherElement = backdrop;
        launcherInput = backdrop.querySelector('.coffee-launcher-input');

        // Close on backdrop click
        backdrop.addEventListener('click', function(e) {
            if (e.target === backdrop) {
                hideLauncher();
            }
        });

        // Close on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && isLauncherVisible) {
                hideLauncher();
            }
        });

        // Handle input
        launcherInput.addEventListener('input', function(e) {
            handleLauncherInput(e.target.value);
        });
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
        toggleLauncher();
    }

    /**
     * Toggle launcher visibility
     */
    function toggleLauncher() {
        if (isLauncherVisible) {
            hideLauncher();
        } else {
            showLauncher();
        }
    }

    /**
     * Show the launcher
     */
    function showLauncher() {
        if (!launcherElement) return;

        launcherElement.classList.add('active');
        isLauncherVisible = true;

        // Focus input after animation starts
        setTimeout(function() {
            launcherInput.focus();
        }, 50);
    }

    /**
     * Hide the launcher
     */
    function hideLauncher() {
        if (!launcherElement) return;

        launcherElement.classList.remove('active');
        isLauncherVisible = false;

        // Clear input
        launcherInput.value = '';

        // Reset results
        var resultsContainer = launcherElement.querySelector('.coffee-launcher-results');
        resultsContainer.innerHTML = `
            <div class="coffee-launcher-empty">
                Start typing to search...
            </div>
        `;
    }

    /**
     * Handle launcher input changes with debouncing
     * @param {string} value - The input value
     */
    function handleLauncherInput(value) {
        var resultsContainer = launcherElement.querySelector('.coffee-launcher-results');

        // Cancel previous debounce timer
        if (searchDebounceTimer) {
            clearTimeout(searchDebounceTimer);
        }

        // Cancel previous search request if still pending
        if (currentSearchRequest) {
            currentSearchRequest.abort();
            currentSearchRequest = null;
        }

        // Handle empty input
        if (!value.trim()) {
            resultsContainer.innerHTML = `
                <div class="coffee-launcher-empty">
                    Start typing to search...
                </div>
            `;
            return;
        }

        // Show loading state
        resultsContainer.innerHTML = `
            <div class="coffee-launcher-empty">
                Searching...
            </div>
        `;

        // Debounce search (300ms delay)
        searchDebounceTimer = setTimeout(function() {
            performSearch(value);
        }, 300);
    }

    /**
     * Perform search via API
     * @param {string} query - The search query
     */
    function performSearch(query) {
        var resultsContainer = launcherElement.querySelector('.coffee-launcher-results');

        // Create AbortController for cancellable requests
        var controller = new AbortController();
        currentSearchRequest = controller;

        // Build search URL
        var searchUrl = '/admin/coffee/search/?q=' + encodeURIComponent(query);

        // Perform fetch request
        fetch(searchUrl, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            signal: controller.signal
        })
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Search failed: ' + response.status);
            }
            return response.json();
        })
        .then(function(data) {
            currentSearchRequest = null;
            displaySearchResults(data.results);
        })
        .catch(function(error) {
            currentSearchRequest = null;

            // Ignore aborted requests
            if (error.name === 'AbortError') {
                return;
            }

            console.error('Search error:', error);
            resultsContainer.innerHTML = `
                <div class="coffee-launcher-empty">
                    Search failed. Please try again.
                </div>
            `;
        });
    }

    /**
     * Display search results in the launcher
     * @param {Array} results - Array of result objects
     */
    function displaySearchResults(results) {
        var resultsContainer = launcherElement.querySelector('.coffee-launcher-results');

        if (!results || results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="coffee-launcher-empty">
                    No results found
                </div>
            `;
            return;
        }

        var html = results.map(function(item) {
            return `
                <div class="coffee-launcher-result-item" data-url="${item.url}">
                    <span class="coffee-launcher-result-icon">${item.icon}</span>
                    <div class="coffee-launcher-result-text">
                        <div class="coffee-launcher-result-title">${item.title}</div>
                        <div class="coffee-launcher-result-subtitle">${item.subtitle}</div>
                    </div>
                </div>
            `;
        }).join('');

        resultsContainer.innerHTML = html;

        // Add click handlers to results
        var items = resultsContainer.querySelectorAll('.coffee-launcher-result-item');
        items.forEach(function(item) {
            item.addEventListener('click', function() {
                handleResultClick(item.dataset.url);
            });
        });
    }

    /**
     * Handle result item click
     * @param {string} url - The URL to navigate to
     */
    function handleResultClick(url) {
        if (url) {
            // Navigate to the selected URL
            window.location.href = url;
        }
        hideLauncher();
    }

    // Expose public API if needed
    window.CoffeeAdmin = {
        init: initCoffeeAdmin,
        version: '0.1.0',
        // Expose keystroke handler for customization
        onKeystrokeTriggered: onKeystrokeTriggered,
        // Launcher controls
        showLauncher: showLauncher,
        hideLauncher: hideLauncher,
        toggleLauncher: toggleLauncher
    };

})();
