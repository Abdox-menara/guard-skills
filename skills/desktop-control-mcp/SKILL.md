---
name: desktop-control-mcp
description: Enhanced Desktop Control MCP Server for advanced Windows PC control with AI/ML integration, enterprise security, and intelligent automation.
---

# Desktop Control MCP Skill

## Overview

Enhanced Desktop Control MCP Server for advanced Windows PC control with AI/ML integration, enterprise security, and intelligent automation.

## Capabilities

### 1. Screenshot and Capture
- take_screenshot() - Full screenshot
- take_region_screenshot(left, top, width, height) - Capture specific region
- screenshot_with_ocr() - Screenshot with OCR text extraction
- compare_screenshots(img1, img2) - Compare screenshots
- wait_for_screen_change(x, y, w, h, timeout) - Wait for screen changes
- record_screen(duration, fps) - Record screen video

### 2. Mouse Automation
- move_mouse(x, y, duration, tween) - Move mouse with easing
- move_mouse_relative(dx, dy) - Move relative to current position
- click(x, y, button, clicks) - Click at position
- double_click(x, y) - Double click
- right_click(x, y) - Right click
- middle_click(x, y) - Middle click
- drag(from_x, from_y, to_x, to_y) - Drag operation
- scroll(amount) - Scroll up/down
- smooth_move(x, y, steps) - Smooth mouse movement
- mouse_position() - Get current position
- screen_size() - Get screen dimensions

### 3. Keyboard Automation
- type_text(text, interval) - Type text
- type_unicode(text) - Type unicode text via clipboard
- press_key(key) - Press single key
- hotkey(keys) - Key combination (e.g., ctrl+c)
- key_down(key) - Hold key
- key_up(key) - Release key
- type_password(password) - Type password securely

### 4. Window Management
- list_windows() - List all visible windows
- activate_window(title) - Focus window by title
- close_window(title) - Close window
- minimize_window(title) - Minimize window
- maximize_window(title) - Maximize window
- restore_window(title) - Restore window
- resize_window(title, width, height) - Resize window
- move_window(title, x, y) - Move window
- window_info(title) - Get window information
- tile_windows_side_by_side(title1, title2) - Tile windows
- set_always_on_top(title) - Set window always on top

### 5. OCR (Optical Character Recognition)
- ocr_screen() - OCR full screen
- ocr_region(left, top, width, height) - OCR specific region
- find_text_on_screen(text) - Find text on screen
- ocr_with_positions(image_path) - OCR with position data

### 6. Clipboard Operations
- clipboard_get() - Get clipboard content
- clipboard_set(text) - Set clipboard content
- clipboard_clear() - Clear clipboard

### 7. Process Management
- list_processes(filter_str) - List running processes
- kill_process(name) - Kill process by name
- process_info(name) - Get process information

### 8. System Information
- system_info() - Comprehensive system information
- get_cpu_usage() - CPU usage
- get_memory_usage() - Memory usage
- get_disk_usage(drive) - Disk usage

### 9. File Operations
- read_file(path) - Read file content
- write_file(path, content) - Write to file
- copy_file(src, dst) - Copy file
- move_file(src, dst) - Move file
- delete_file(path) - Delete file
- make_directory(path) - Create directory
- find_files(pattern) - Find files
- file_exists(path) - Check if file exists
- get_file_info(path) - Get file information
- get_directory_size(path) - Get directory size

### 10. Command Execution
- run_command(command) - Run command prompt command
- run_powershell(script) - Run PowerShell command
- open_file(path) - Open file with default application
- open_url(url) - Open URL in default browser

### 11. Network Operations
- ping(host) - Ping host
- get_ip() - Get local IP
- is_connected() - Check internet connectivity
- get_public_ip() - Get public IP

### 12. Registry Operations (Windows)
- read_registry(hive, path, name) - Read registry value
- write_registry(hive, path, name, value) - Write registry value

### 13. Service Management
- list_services() - List all services
- service_status(name) - Get service status
- start_service(name) - Start service
- stop_service(name) - Stop service

### 14. Scheduled Tasks
- list_scheduled_tasks() - List scheduled tasks

### 15. WiFi Management
- get_wifi_networks() - Get available WiFi networks
- connect_wifi(ssid, password) - Connect to WiFi

### 16. System Control
- lock_screen() - Lock screen
- set_wallpaper(path) - Set desktop wallpaper
- show_notification(title, message) - Show notification

### 17. Image Recognition
- find_image_on_screen(image_path, confidence) - Find image on screen
- click_image_on_screen(image_path, confidence) - Click on image
- wait_for_image(image_path, timeout) - Wait for image

### 18. Pixel Color
- get_pixel(x, y) - Get pixel color
- pixel_matches_color(x, y, r, g, b, tolerance) - Check pixel color

### 19. Advanced Automation
- record_macro(duration, save_to) - Record mouse/keyboard actions
- create_automation_script(actions, save_to) - Create automation script
- quick_reference() - Get quick reference

