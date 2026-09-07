import json

with open("d:/Exam/data.json", "r", encoding="utf-8") as f:
    app_data = json.load(f)

courses_json = json.dumps(app_data["courses"])
advisors_json = json.dumps(app_data["advisors"])
timings_json = json.dumps(app_data["examTimings"])

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UIU Pre-Advising & Exam Routine Assistant - Fall 2026</title>
    <meta name="description" content="Official UIU Pre-Advising & Exam Routine Planner for Fall 2026. Complete 12 trimesters, exact Mid and Final exam timings, clash detection, and advisor lookup for BSCSE and BSDS.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #f97316; /* UIU Orange */
            --primary-hover: #ea580c;
            --primary-glow: rgba(249, 115, 22, 0.25);
            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --accent-glow: rgba(99, 102, 241, 0.25);
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.2);
            --danger: #ef4444;
            --danger-glow: rgba(239, 68, 68, 0.25);
            --warning: #f59e0b;

            --bg: #0b0f19;
            --surface: #111827;
            --surface-card: #1e293b;
            --surface-hover: #283548;
            --border: #334155;
            --border-light: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
            --glass-bg: rgba(17, 24, 39, 0.85);
            --glass-border: rgba(255, 255, 255, 0.08);
            --slot-badge-bg: rgba(99, 102, 241, 0.15);
            --slot-badge-color: #a5b4fc;
        }

        [data-theme="light"] {
            --bg: #f8fafc;
            --surface: #ffffff;
            --surface-card: #ffffff;
            --surface-hover: #f1f5f9;
            --border: #e2e8f0;
            --border-light: #f1f5f9;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --text-dim: #94a3b8;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
            --glass-bg: rgba(255, 255, 255, 0.9);
            --glass-border: rgba(0, 0, 0, 0.08);
            --slot-badge-bg: #eff6ff;
            --slot-badge-color: #2563eb;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.5;
            transition: background-color 0.25s ease, color 0.25s ease;
        }

        /* Header Bar */
        header {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--glass-border);
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }

        .header-inner {
            max-width: 1440px;
            margin: 0 auto;
            padding: 0.85rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.5rem;
            flex-wrap: wrap;
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            text-decoration: none;
        }

        .logo-circle {
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
            font-size: 1.25rem;
            box-shadow: 0 4px 14px var(--primary-glow);
        }

        .brand-text h1 {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .brand-text p {
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        .badge-term {
            font-size: 0.7rem;
            padding: 2px 8px;
            background: rgba(249, 115, 22, 0.15);
            color: #f97316;
            border-radius: 9999px;
            font-weight: 700;
            border: 1px solid rgba(249, 115, 22, 0.3);
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        /* Routine Mode Switcher (Mid vs Final) */
        .routine-toggle {
            display: inline-flex;
            background: var(--surface);
            padding: 3px;
            border-radius: 10px;
            border: 1px solid var(--border);
        }

        .routine-toggle button {
            background: transparent;
            border: none;
            padding: 0.45rem 0.9rem;
            font-size: 0.825rem;
            font-weight: 600;
            color: var(--text-muted);
            border-radius: 7px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .routine-toggle button.active {
            background: var(--accent);
            color: white;
            box-shadow: 0 2px 8px var(--accent-glow);
        }

        .header-btn {
            background: var(--surface);
            color: var(--text-main);
            border: 1px solid var(--border);
            padding: 0.5rem 0.9rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            transition: all 0.2s ease;
        }

        .header-btn:hover {
            background: var(--surface-hover);
            border-color: var(--text-muted);
        }

        .header-btn.primary {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
            box-shadow: 0 2px 10px var(--primary-glow);
        }

        .header-btn.primary:hover {
            background: var(--primary-hover);
        }

        /* Stat Bar */
        .stats-bar {
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 0.65rem 1.5rem;
        }

        .stats-inner {
            max-width: 1440px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .stat-chips {
            display: flex;
            align-items: center;
            gap: 1.25rem;
            flex-wrap: wrap;
        }

        .stat-chip {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
        }

        .stat-chip .val {
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text-main);
        }

        .stat-chip .status-pill {
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .status-pill.normal {
            background: rgba(16, 185, 129, 0.15);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .status-pill.underload {
            background: rgba(245, 158, 11, 0.15);
            color: #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .status-pill.overload {
            background: rgba(239, 68, 68, 0.15);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        /* Clash Banner Alert */
        .clash-alert {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.25) 100%);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #fca5a5;
            padding: 1rem 1.5rem;
            margin: 1.5rem auto 0;
            max-width: 1440px;
            border-radius: 12px;
            display: none;
            animation: pulse-border 2s infinite ease-in-out;
        }

        .clash-alert.active {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }

        @keyframes pulse-border {
            0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.3); }
            50% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0.15); }
        }

        .clash-icon {
            font-size: 1.6rem;
            line-height: 1;
        }

        .clash-content h3 {
            font-size: 1rem;
            font-weight: 700;
            color: #f87171;
            margin-bottom: 0.35rem;
        }

        .clash-list {
            list-style: none;
            font-size: 0.875rem;
            color: #fecaca;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .clash-list li {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .clash-list li::before {
            content: "•";
            color: #ef4444;
            font-weight: bold;
        }

        /* Main Container */
        .main-container {
            max-width: 1440px;
            margin: 1.5rem auto 3rem;
            padding: 0 1.5rem;
            display: grid;
            grid-template-columns: 1fr 440px;
            gap: 1.75rem;
            align-items: start;
        }

        @media (max-width: 1100px) {
            .main-container {
                grid-template-columns: 1fr;
            }
            .sidebar {
                position: static !important;
            }
        }

        /* Card styles */
        .card {
            background: var(--surface);
            border-radius: 16px;
            border: 1px solid var(--border);
            box-shadow: var(--card-shadow);
            overflow: hidden;
        }

        .card-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            background: rgba(255, 255, 255, 0.01);
        }

        .card-header h2 {
            font-size: 1.15rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-body {
            padding: 1.5rem;
        }

        /* App Primary Tabs (Catalog / Advisor / Routine) */
        .nav-tabs {
            display: flex;
            gap: 0.5rem;
            padding: 0.5rem 1.5rem;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            overflow-x: auto;
        }

        .nav-tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: 600;
            padding: 0.6rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            white-space: nowrap;
            transition: all 0.2s ease;
        }

        .nav-tab-btn:hover {
            color: var(--text-main);
            background: var(--surface-hover);
        }

        .nav-tab-btn.active {
            color: white;
            background: var(--accent);
            box-shadow: 0 2px 8px var(--accent-glow);
        }

        /* Trimester Filter Tabs */
        .trimester-pills {
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
            margin-bottom: 1.25rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-light);
        }

        .tri-pill {
            background: var(--surface-card);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 0.35rem 0.75rem;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .tri-pill:hover {
            color: var(--text-main);
            border-color: var(--text-muted);
        }

        .tri-pill.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
            box-shadow: 0 2px 8px var(--primary-glow);
        }

        /* Search & Filter Bar */
        .filter-controls {
            display: flex;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }

        .search-box-wrapper {
            position: relative;
            flex: 1;
            min-width: 260px;
        }

        .search-icon {
            position: absolute;
            left: 0.9rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-dim);
            pointer-events: none;
        }

        .search-input {
            width: 100%;
            padding: 0.75rem 1rem 0.75rem 2.6rem;
            background: var(--surface-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            color: var(--text-main);
            font-size: 0.9rem;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .select-filter {
            padding: 0.75rem 1rem;
            background: var(--surface-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            color: var(--text-main);
            font-size: 0.875rem;
            cursor: pointer;
        }

        .select-filter:focus {
            outline: none;
            border-color: var(--accent);
        }

        /* Trimester Section & Course Rows */
        .tri-section {
            margin-bottom: 1.5rem;
            background: var(--surface-card);
            border-radius: 14px;
            border: 1px solid var(--border);
            overflow: hidden;
            transition: border-color 0.2s;
        }

        .tri-header {
            padding: 0.85rem 1.25rem;
            background: rgba(255, 255, 255, 0.02);
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            user-select: none;
            border-bottom: 1px solid var(--border-light);
        }

        .tri-header:hover {
            background: var(--surface-hover);
        }

        .tri-header-title {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            font-size: 0.95rem;
            font-weight: 700;
        }

        .tri-badge-count {
            font-size: 0.75rem;
            padding: 2px 7px;
            border-radius: 9999px;
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-muted);
        }

        .tri-toggle-icon {
            font-size: 0.8rem;
            color: var(--text-muted);
            transition: transform 0.2s ease;
        }

        .tri-section.collapsed .tri-toggle-icon {
            transform: rotate(-90deg);
        }

        .tri-section.collapsed .courses-table {
            display: none;
        }

        /* Courses Table */
        .courses-table {
            display: flex;
            flex-direction: column;
        }

        .course-item {
            display: grid;
            grid-template-columns: 44px 110px 1fr 70px 220px;
            align-items: center;
            padding: 0.9rem 1.25rem;
            border-bottom: 1px solid var(--border-light);
            gap: 0.85rem;
            transition: background 0.15s ease;
            position: relative;
        }

        .course-item:last-child {
            border-bottom: none;
        }

        .course-item:hover {
            background: var(--surface-hover);
        }

        .course-item.selected {
            background: rgba(16, 185, 129, 0.06);
            border-left: 4px solid var(--success);
        }

        .course-item.has-clash {
            background: rgba(239, 68, 68, 0.08) !important;
            border-left: 4px solid var(--danger) !important;
        }

        .custom-checkbox {
            width: 22px;
            height: 22px;
            cursor: pointer;
            accent-color: var(--primary);
        }

        .c-code-box {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .c-code {
            font-weight: 700;
            font-size: 0.9rem;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
        }

        .c-alt {
            font-size: 0.7rem;
            color: var(--text-dim);
        }

        .c-title-box {
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
        }

        .c-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-main);
        }

        .c-meta {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .meta-pill {
            font-size: 0.725rem;
            padding: 2px 7px;
            border-radius: 5px;
            font-weight: 500;
        }

        .meta-pill.prereq {
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-muted);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .meta-pill.major {
            background: rgba(99, 102, 241, 0.15);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        .meta-pill.note {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .c-cr {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-muted);
            text-align: center;
        }

        .c-exam-time {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
            font-size: 0.775rem;
        }

        .exam-slot-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 3px 8px;
            border-radius: 6px;
            background: var(--slot-badge-bg);
            color: var(--slot-badge-color);
            font-weight: 600;
            width: fit-content;
        }

        .exam-slot-pill.no-exam {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-dim);
        }

        .exact-time-text {
            font-size: 0.725rem;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
        }

        @media (max-width: 768px) {
            .course-item {
                grid-template-columns: 36px 1fr;
                gap: 0.5rem;
            }
            .c-cr, .c-exam-time {
                grid-column: 2;
            }
        }

        /* Sidebar & Timetable */
        .sidebar {
            position: sticky;
            top: 90px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .selected-box {
            max-height: 280px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            padding-right: 0.25rem;
        }

        .selected-pill {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.65rem 0.9rem;
            background: var(--surface-card);
            border-radius: 10px;
            border: 1px solid var(--border);
            font-size: 0.85rem;
            transition: all 0.15s ease;
        }

        .selected-pill:hover {
            border-color: var(--text-muted);
        }

        .selected-pill.clash-pill {
            border-color: var(--danger);
            background: rgba(239, 68, 68, 0.1);
        }

        .remove-pill-btn {
            background: none;
            border: none;
            color: var(--danger);
            cursor: pointer;
            font-size: 1.1rem;
            padding: 0 4px;
            line-height: 1;
            font-weight: bold;
            opacity: 0.7;
            transition: opacity 0.15s;
        }

        .remove-pill-btn:hover {
            opacity: 1;
        }

        /* Exam Matrix Timetable */
        .timetable-wrapper {
            overflow-x: auto;
        }

        .timetable {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.785rem;
            text-align: center;
        }

        .timetable th {
            background: rgba(255, 255, 255, 0.04);
            color: var(--text-muted);
            padding: 0.65rem 0.4rem;
            border: 1px solid var(--border);
            font-weight: 700;
            font-size: 0.75rem;
        }

        .timetable td {
            border: 1px solid var(--border);
            padding: 0.45rem 0.35rem;
            height: 48px;
            vertical-align: middle;
            transition: background 0.15s;
        }

        .timetable td.day-col {
            font-weight: 700;
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-main);
            width: 60px;
        }

        .cell-course-badge {
            display: inline-block;
            padding: 3px 6px;
            border-radius: 5px;
            font-size: 0.7rem;
            font-weight: 700;
            margin: 2px;
            font-family: 'JetBrains Mono', monospace;
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.4);
        }

        .cell-course-badge.clash {
            background: rgba(239, 68, 68, 0.25) !important;
            color: #fca5a5 !important;
            border: 1px solid #ef4444 !important;
            animation: bounce 0.5s ease;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-3px); }
        }

        /* Advisor Lookup Card */
        .advisor-panel {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .advisor-search-row {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .advisor-result-card {
            background: var(--surface-card);
            border-radius: 14px;
            border: 1px solid var(--border);
            padding: 1.5rem;
            display: none;
            flex-direction: column;
            gap: 1rem;
        }

        .advisor-result-card.active {
            display: flex;
            animation: fadeIn 0.2s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .advisor-head {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .advisor-avatar {
            width: 52px;
            height: 52px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent) 0%, #4338ca 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.4rem;
            font-weight: 800;
        }

        .advisor-details {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .advisor-field {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            font-size: 0.875rem;
            color: var(--text-main);
        }

        .advisor-field a {
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
        }

        .advisor-field a:hover {
            text-decoration: underline;
        }

        /* Full University Routine Tab */
        .full-routine-grid {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .routine-day-card {
            background: var(--surface-card);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
        }

        .routine-day-header {
            background: rgba(255, 255, 255, 0.03);
            padding: 0.75rem 1.25rem;
            font-weight: 700;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .routine-slots-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1px;
            background: var(--border);
        }

        @media (max-width: 768px) {
            .routine-slots-grid {
                grid-template-columns: 1fr;
            }
        }

        .routine-slot-col {
            background: var(--surface-card);
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .routine-slot-title {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--accent);
            display: flex;
            justify-content: space-between;
            padding-bottom: 0.35rem;
            border-bottom: 1px solid var(--border-light);
        }

        .routine-course-pill {
            font-size: 0.775rem;
            padding: 4px 8px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-light);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .routine-course-pill.is-user-selected {
            background: rgba(249, 115, 22, 0.2);
            border-color: var(--primary);
            color: var(--primary);
            font-weight: 700;
        }

        /* Print Media Styling */
        @media print {
            header, .filter-controls, .trimester-pills, .nav-tabs, .header-actions, .btn-reset, .remove-pill-btn {
                display: none !important;
            }
            body {
                background: white !important;
                color: black !important;
            }
            .main-container {
                display: block !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            .card {
                border: 1px solid #ccc !important;
                box-shadow: none !important;
                margin-bottom: 1.5rem !important;
            }
            .timetable th, .timetable td {
                border: 1px solid #666 !important;
                color: black !important;
            }
        }
    </style>
</head>
<body data-theme="dark">

<header>
    <div class="header-inner">
        <a href="#" class="brand-container">
            <div class="logo-circle">U</div>
            <div class="brand-text">
                <h1>UIU Pre-Advising & Exam Planner <span class="badge-term">Fall 2026</span></h1>
                <p>Dept. of CSE & Data Science • United International University</p>
            </div>
        </a>

        <div class="header-actions">
            <div class="routine-toggle">
                <button id="midBtn" class="active" onclick="setExamMode('MID')">Mid Exam</button>
                <button id="finalBtn" onclick="setExamMode('FINAL')">Final Exam</button>
            </div>

            <button class="header-btn" onclick="toggleTheme()" id="themeBtn" title="Toggle Theme">
                <span id="themeIcon">☀️</span> <span id="themeText">Light</span>
            </button>

            <button class="header-btn primary" onclick="window.print()" title="Print Routine Slip">
                🖨️ Print Routine
            </button>
        </div>
    </div>
</header>

<div class="stats-bar">
    <div class="stats-inner">
        <div class="stat-chips">
            <div class="stat-chip">
                <span>Selected Courses:</span>
                <span class="val" id="selectedCount">0</span>
            </div>
            <div class="stat-chip">
                <span>Total Credits:</span>
                <span class="val" id="totalCredits">0</span>
                <span class="status-pill underload" id="creditStatus">Underload (&lt; 9 Cr)</span>
            </div>
            <div class="stat-chip">
                <span>Exam Mode:</span>
                <span class="val" id="currentModeLabel" style="color: var(--accent);">Mid Exam Schedule</span>
            </div>
        </div>

        <div>
            <button class="header-btn" onclick="resetSelections()" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;">
                Clear Selection
            </button>
        </div>
    </div>
</div>

<!-- Clash Alert Banner -->
<div class="clash-alert" id="clashAlertBanner">
    <div class="clash-icon">⚠️</div>
    <div class="clash-content">
        <h3>Exam Schedule Conflict Detected!</h3>
        <p style="font-size: 0.85rem; margin-bottom: 0.5rem;">
            The following selected courses take place at the exact same day and time slot:
        </p>
        <ul class="clash-list" id="clashItemsList"></ul>
    </div>
</div>

<main class="main-container">
    <!-- Left Column: Catalog / Advisor / Routine -->
    <section>
        <div class="card">
            <div class="nav-tabs">
                <button class="nav-tab-btn active" id="tabCoursesBtn" onclick="switchNavTab('courses')">
                    📚 Course Catalog (12 Trimesters)
                </button>
                <button class="nav-tab-btn" id="tabAdvisorBtn" onclick="switchNavTab('advisor')">
                    👨‍🏫 Faculty Advisor Lookup
                </button>
                <button class="nav-tab-btn" id="tabRoutineBtn" onclick="switchNavTab('routine')">
                    🗓️ Full University Routine
                </button>
            </div>

            <!-- View 1: Course Catalog -->
            <div class="card-body" id="viewCourses">
                <!-- Trimester Quick Filter Pills -->
                <div class="trimester-pills" id="trimesterPills">
                    <button class="tri-pill active" onclick="filterTrimester('ALL')">All</button>
                </div>

                <!-- Search & Filters -->
                <div class="filter-controls">
                    <div class="search-box-wrapper">
                        <span class="search-icon">🔍</span>
                        <input type="text" id="courseSearch" class="search-input" placeholder="Search by course code, title, prerequisite (e.g. CSE 1111, Calculus)...">
                    </div>

                    <select id="categoryFilter" class="select-filter" onchange="applyFilters()">
                        <option value="ALL">All Categories</option>
                        <option value="Core">Core Courses</option>
                        <option value="Capstone">Capstone FYDP (I, II, III)</option>
                        <option value="GED Optional">GED Optionals</option>
                        <option value="Elective">All Electives</option>
                        <option value="BSDS Core">BSDS (Data Science)</option>
                    </select>

                    <select id="examDayFilter" class="select-filter" onchange="applyFilters()">
                        <option value="ALL">All Exam Days</option>
                        <option value="Day 1">Day 1</option>
                        <option value="Day 2">Day 2</option>
                        <option value="Day 3">Day 3</option>
                        <option value="Day 4">Day 4</option>
                        <option value="Day 5">Day 5</option>
                        <option value="Day 6">Day 6</option>
                        <option value="Day 7">Day 7</option>
                        <option value="N/A">No Written Exam</option>
                    </select>
                </div>

                <!-- Catalog Container -->
                <div id="catalogContainer"></div>
            </div>

            <!-- View 2: Advisor Lookup -->
            <div class="card-body" id="viewAdvisor" style="display: none;">
                <div class="advisor-panel">
                    <div>
                        <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.35rem;">Find Your Assigned Faculty Advisor</h3>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">
                            Enter your official UIU Student ID to instantly view your advisor's name, phone number, email, and office room.
                        </p>
                    </div>

                    <div class="advisor-search-row">
                        <select id="advisorProgram" class="select-filter" onchange="lookupAdvisor()" style="min-width: 140px;">
                            <option value="BSCSE">B.Sc. in CSE</option>
                            <option value="BSDS">B.Sc. in Data Science</option>
                        </select>
                        <div class="search-box-wrapper">
                            <span class="search-icon">🎓</span>
                            <input type="text" id="advisorStudentId" class="search-input" placeholder="Enter Student ID (e.g. 0112620055 or 0152620010)..." oninput="lookupAdvisor()">
                        </div>
                    </div>

                    <!-- Result Card -->
                    <div class="advisor-result-card" id="advisorResultCard">
                        <div class="advisor-head">
                            <div class="advisor-avatar" id="advAvatar">👨‍🏫</div>
                            <div>
                                <h4 id="advName" style="font-size: 1.15rem; font-weight: 700;">-</h4>
                                <span class="badge-term" id="advBatch">-</span>
                            </div>
                        </div>
                        <div class="advisor-details">
                            <div class="advisor-field">
                                <span>📞</span> <strong>Direct Cell:</strong> <a id="advCell" href="#">-</a>
                            </div>
                            <div class="advisor-field">
                                <span>📧</span> <strong>Email:</strong> <a id="advEmail" href="#">-</a>
                            </div>
                            <div class="advisor-field">
                                <span>📍</span> <strong>Office Room:</strong> <span id="advOffice" style="font-weight: 600;">-</span>
                            </div>
                            <div class="advisor-field">
                                <span>🆔</span> <strong>ID Batch Range:</strong> <span id="advRange" style="color: var(--text-muted);">-</span>
                            </div>
                        </div>
                    </div>

                    <!-- Complete Advisor Directory Table -->
                    <div style="margin-top: 1.5rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                            <h4 style="font-size: 0.95rem; font-weight: 700;">Complete Advisor Directory (Fall 2026)</h4>
                            <input type="text" id="advisorFilterText" placeholder="Filter faculty..." class="search-input" style="width: 220px; padding: 0.4rem 0.8rem; font-size: 0.8rem;" oninput="renderAdvisorTable()">
                        </div>
                        <div style="max-height: 400px; overflow-y: auto; border: 1px solid var(--border); border-radius: 10px;">
                            <table style="width: 100%; border-collapse: collapse; font-size: 0.825rem; text-align: left;">
                                <thead>
                                    <tr style="background: var(--surface-card); position: sticky; top: 0; border-bottom: 1px solid var(--border);">
                                        <th style="padding: 0.6rem 0.8rem;">Batch</th>
                                        <th style="padding: 0.6rem 0.8rem;">Advisor Name</th>
                                        <th style="padding: 0.6rem 0.8rem;">Office</th>
                                        <th style="padding: 0.6rem 0.8rem;">Contact</th>
                                    </tr>
                                </thead>
                                <tbody id="advisorDirectoryBody"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- View 3: Full University Routine -->
            <div class="card-body" id="viewRoutine" style="display: none;">
                <div style="margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="font-size: 1.1rem; font-weight: 700;">Full Fall 2026 Examination Schedule</h3>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">
                            Courses highlighted in <span style="color: var(--primary); font-weight: bold;">orange</span> are currently in your selected courses list.
                        </p>
                    </div>
                </div>
                <div class="full-routine-grid" id="fullRoutineGrid"></div>
            </div>
        </div>
    </section>

    <!-- Right Column: Sticky Selected Courses & Visual Timetable -->
    <aside class="sidebar">
        <!-- Selected Courses Card -->
        <div class="card">
            <div class="card-header">
                <h2><span>📋</span> Selected Courses</h2>
                <span class="badge-term" id="selectedCrBadge">0 Credits</span>
            </div>
            <div class="card-body">
                <div class="selected-box" id="selectedCoursesList">
                    <p style="color: var(--text-dim); font-size: 0.85rem; text-align: center; padding: 1.5rem 0;">
                        No courses selected yet.<br>Click any course checkbox to begin planning!
                    </p>
                </div>
            </div>
        </div>

        <!-- Timetable Matrix Card -->
        <div class="card">
            <div class="card-header">
                <h2><span>🗓️</span> Weekly Exam Timetable</h2>
                <span style="font-size: 0.75rem; color: var(--accent); font-weight: 700;" id="tableModeTag">MID EXAM</span>
            </div>
            <div class="card-body" style="padding: 1rem;">
                <div class="timetable-wrapper">
                    <table class="timetable" id="examTimetable">
                        <thead>
                            <tr>
                                <th>Day</th>
                                <th>
                                    <div>T1</div>
                                    <div style="font-size: 0.65rem; font-weight: normal; color: var(--text-muted);">09:00 - 11:00 AM</div>
                                </th>
                                <th>
                                    <div>T2</div>
                                    <div style="font-size: 0.65rem; font-weight: normal; color: var(--text-muted);">11:30 - 01:30 PM</div>
                                </th>
                                <th>
                                    <div>T3</div>
                                    <div style="font-size: 0.65rem; font-weight: normal; color: var(--text-muted);" id="t3HeaderTime">02:00 - 04:00 PM</div>
                                </th>
                            </tr>
                        </thead>
                        <tbody id="timetableBody"></tbody>
                    </table>
                </div>

                <div style="margin-top: 1rem; padding: 0.75rem; background: var(--surface-card); border-radius: 8px; font-size: 0.75rem; color: var(--text-muted); line-height: 1.4;">
                    💡 <strong>Timetable Tip:</strong> Midterm T3 slot is 2:00–4:00 PM, while Final Exam T3 slot is 2:30–4:30 PM. Courses marked <em>(Only Final Exam)</em> will not have midterm exams.
                </div>
            </div>
        </div>
    </aside>
</main>

<script>
    // Embedded Complete Datasets
    const COURSES_DATA = __COURSES_JSON__;
    const ADVISORS_DATA = __ADVISORS_JSON__;
    const TIMINGS_DATA = __TIMINGS_JSON__;

    let selectedCodes = new Set();
    let currentExamMode = 'MID'; // 'MID' or 'FINAL'
    let currentTrimesterFilter = 'ALL';
    let currentNavTab = 'courses';

    // DOM Elements
    const catalogContainer = document.getElementById('catalogContainer');
    const selectedListEl = document.getElementById('selectedCoursesList');
    const selectedCountEl = document.getElementById('selectedCount');
    const totalCreditsEl = document.getElementById('totalCredits');
    const selectedCrBadge = document.getElementById('selectedCrBadge');
    const creditStatusEl = document.getElementById('creditStatus');
    const clashBanner = document.getElementById('clashAlertBanner');
    const clashItemsList = document.getElementById('clashItemsList');
    const timetableBody = document.getElementById('timetableBody');
    const currentModeLabel = document.getElementById('currentModeLabel');
    const tableModeTag = document.getElementById('tableModeTag');
    const t3HeaderTime = document.getElementById('t3HeaderTime');
    const searchInput = document.getElementById('courseSearch');
    const categoryFilter = document.getElementById('categoryFilter');
    const examDayFilter = document.getElementById('examDayFilter');
    const trimesterPillsContainer = document.getElementById('trimesterPills');

    // Initialize App
    function init() {
        buildTrimesterFilterPills();
        renderCatalog();
        renderTimetable();
        renderFullRoutine();
        renderAdvisorTable();

        searchInput.addEventListener('input', applyFilters);
        categoryFilter.addEventListener('change', applyFilters);
        examDayFilter.addEventListener('change', applyFilters);

        // Keyboard shortcut '/' to search
        window.addEventListener('keydown', (e) => {
            if (e.key === '/' && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // Build 12 Trimester Tabs
    function buildTrimesterFilterPills() {
        trimesterPillsContainer.innerHTML = `
            <button class="tri-pill active" onclick="filterTrimester('ALL')">All (1-12)</button>
        `;
        for (let i = 1; i <= 12; i++) {
            const btn = document.createElement('button');
            btn.className = 'tri-pill';
            btn.innerText = `Tri ${i}`;
            btn.onclick = () => filterTrimester(i);
            trimesterPillsContainer.appendChild(btn);
        }
        // GED and Elective pills
        const gedBtn = document.createElement('button');
        gedBtn.className = 'tri-pill';
        gedBtn.innerText = 'GED Optionals';
        gedBtn.onclick = () => filterTrimester('GED');
        trimesterPillsContainer.appendChild(gedBtn);

        const elecBtn = document.createElement('button');
        elecBtn.className = 'tri-pill';
        elecBtn.innerText = 'Elective Tracks';
        elecBtn.onclick = () => filterTrimester('Elective');
        trimesterPillsContainer.appendChild(elecBtn);

        const dsBtn = document.createElement('button');
        dsBtn.className = 'tri-pill';
        dsBtn.innerText = 'BSDS Core';
        dsBtn.onclick = () => filterTrimester('BSDS');
        trimesterPillsContainer.appendChild(dsBtn);
    }

    function filterTrimester(tri) {
        currentTrimesterFilter = tri;
        document.querySelectorAll('.tri-pill').forEach(btn => {
            if (tri === 'ALL' && btn.innerText.includes('All')) btn.classList.add('active');
            else if (btn.innerText === `Tri ${tri}`) btn.classList.add('active');
            else if (tri === 'GED' && btn.innerText.includes('GED')) btn.classList.add('active');
            else if (tri === 'Elective' && btn.innerText.includes('Elective')) btn.classList.add('active');
            else if (tri === 'BSDS' && btn.innerText.includes('BSDS')) btn.classList.add('active');
            else btn.classList.remove('active');
        });
        applyFilters();
    }

    // Exam Mode Toggle
    function setExamMode(mode) {
        currentExamMode = mode;
        document.getElementById('midBtn').classList.toggle('active', mode === 'MID');
        document.getElementById('finalBtn').classList.toggle('active', mode === 'FINAL');
        currentModeLabel.innerText = mode === 'MID' ? 'Mid Exam Schedule' : 'Final Exam Schedule';
        tableModeTag.innerText = mode === 'MID' ? 'MID EXAM' : 'FINAL EXAM';
        t3HeaderTime.innerText = mode === 'MID' ? '02:00 - 04:00 PM' : '02:30 - 04:30 PM';

        renderCatalog();
        renderTimetable();
        renderFullRoutine();
    }

    // Filter Logic
    function applyFilters() {
        renderCatalog();
    }

    // Render Course Catalog
    function renderCatalog() {
        const query = (searchInput.value || '').trim().toLowerCase();
        const cat = categoryFilter.value;
        const day = examDayFilter.value;

        catalogContainer.innerHTML = '';

        // Filter courses
        const filtered = COURSES_DATA.filter(c => {
            // Trimester filter
            if (currentTrimesterFilter !== 'ALL' && c.tri != currentTrimesterFilter) {
                return false;
            }
            // Category filter
            if (cat !== 'ALL' && c.category !== cat) {
                return false;
            }
            // Exam Day filter
            if (day !== 'ALL' && c.day !== day) {
                return false;
            }
            // Text search
            if (query) {
                const matchCode = c.code.toLowerCase().includes(query);
                const matchTitle = c.title.toLowerCase().includes(query);
                const matchPre = c.pre.toLowerCase().includes(query);
                const matchAlt = c.alt && c.alt.toLowerCase().includes(query);
                const matchMajor = c.major && c.major.toLowerCase().includes(query);
                if (!matchCode && !matchTitle && !matchPre && !matchAlt && !matchMajor) {
                    return false;
                }
            }
            return true;
        });

        if (filtered.length === 0) {
            catalogContainer.innerHTML = `
                <div style="text-align: center; padding: 3rem 1rem; color: var(--text-dim);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
                    <p style="font-weight: 600;">No courses matched your search criteria.</p>
                    <p style="font-size: 0.85rem; margin-top: 0.25rem;">Try adjusting your query or resetting filters.</p>
                </div>
            `;
            return;
        }

        // Group courses by Trimester / Section
        const groups = {};
        filtered.forEach(c => {
            let key = typeof c.tri === 'number' ? `Trimester ${c.tri}` : c.tri;
            if (!groups[key]) groups[key] = [];
            groups[key].push(c);
        });

        // Compute clashing codes currently
        const clashingCodes = getClashingCourseCodes();

        // Render each section
        Object.keys(groups).forEach(groupKey => {
            const section = document.createElement('div');
            section.className = 'tri-section';

            const header = document.createElement('div');
            header.className = 'tri-header';
            header.innerHTML = `
                <div class="tri-header-title">
                    <span>${groupKey}</span>
                    <span class="tri-badge-count">${groups[groupKey].length} courses</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <button class="header-btn" style="padding: 0.25rem 0.6rem; font-size: 0.725rem;" onclick="event.stopPropagation(); selectAllSection('${groupKey}')">
                        Select All
                    </button>
                    <span class="tri-toggle-icon">▼</span>
                </div>
            `;
            header.onclick = () => section.classList.toggle('collapsed');

            const table = document.createElement('div');
            table.className = 'courses-table';

            groups[groupKey].forEach(c => {
                const isSelected = selectedCodes.has(c.code);
                const isClashing = isSelected && clashingCodes.has(c.code);

                // Determine exact exam time string
                let examTimeDisplay = '';
                if (c.day !== 'N/A' && c.slot !== 'N/A') {
                    const exactTime = TIMINGS_DATA[currentExamMode][c.slot];
                    const noteText = c.note ? ` • ${c.note}` : '';
                    examTimeDisplay = `
                        <div class="exam-slot-pill">
                            📅 ${c.day} • Slot ${c.slot}
                        </div>
                        <div class="exact-time-text">
                            🕒 ${exactTime}${noteText}
                        </div>
                    `;
                } else {
                    examTimeDisplay = `
                        <div class="exam-slot-pill no-exam">
                            🔬 No Written Exam
                        </div>
                        <div class="exact-time-text">Lab / Capstone Evaluation</div>
                    `;
                }

                const item = document.createElement('div');
                item.className = `course-item ${isSelected ? 'selected' : ''} ${isClashing ? 'has-clash' : ''}`;
                item.id = `course-row-${c.code.replace(/\\s+/g, '-')}`;

                item.innerHTML = `
                    <div>
                        <input type="checkbox" class="custom-checkbox" ${isSelected ? 'checked' : ''} onchange="toggleCourse('${c.code}')">
                    </div>
                    <div class="c-code-box">
                        <span class="c-code">${c.code}</span>
                        ${c.alt ? `<span class="c-alt">(${c.alt})</span>` : ''}
                    </div>
                    <div class="c-title-box">
                        <span class="c-title">${c.title}</span>
                        <div class="c-meta">
                            <span class="meta-pill prereq">Pre: ${c.pre}</span>
                            ${c.major ? `<span class="meta-pill major">${c.major}</span>` : ''}
                            ${c.note ? `<span class="meta-pill note">⚡ ${c.note}</span>` : ''}
                        </div>
                    </div>
                    <div class="c-cr">${c.cr} Cr</div>
                    <div class="c-exam-time">
                        ${examTimeDisplay}
                    </div>
                `;

                table.appendChild(item);
            });

            section.appendChild(header);
            section.appendChild(table);
            catalogContainer.appendChild(section);
        });
    }

    // Toggle Course Selection
    function toggleCourse(code) {
        if (selectedCodes.has(code)) {
            selectedCodes.delete(code);
        } else {
            selectedCodes.add(code);
        }
        updateAppUI();
    }

    function selectAllSection(groupKey) {
        const matches = COURSES_DATA.filter(c => {
            let key = typeof c.tri === 'number' ? `Trimester ${c.tri}` : c.tri;
            return key === groupKey;
        });
        matches.forEach(c => selectedCodes.add(c.code));
        updateAppUI();
    }

    // Calculate Clashes
    function checkClashes() {
        const selected = Array.from(selectedCodes).map(code => COURSES_DATA.find(c => c.code === code)).filter(Boolean);
        const clashes = [];
        const clashCodes = new Set();

        for (let i = 0; i < selected.length; i++) {
            for (let j = i + 1; j < selected.length; j++) {
                const c1 = selected[i];
                const c2 = selected[j];

                // If in Mid exam mode and one course is 'Only Final Exam', no midterm clash
                if (currentExamMode === 'MID' && (c1.note === 'Only Final Exam' || c2.note === 'Only Final Exam')) {
                    continue;
                }

                if (c1.day !== 'N/A' && c1.day === c2.day && c1.slot === c2.slot) {
                    const exactTime = TIMINGS_DATA[currentExamMode][c1.slot];
                    clashes.push({
                        c1: c1.code,
                        t1: c1.title,
                        c2: c2.code,
                        t2: c2.title,
                        day: c1.day,
                        slot: c1.slot,
                        time: exactTime
                    });
                    clashCodes.add(c1.code);
                    clashCodes.add(c2.code);
                }
            }
        }

        if (clashes.length > 0) {
            clashBanner.classList.add('active');
            clashItemsList.innerHTML = clashes.map(cl => `
                <li>
                    <strong>${cl.c1}</strong> and <strong>${cl.c2}</strong> clash on 
                    <span style="color: white; font-weight: 600;">${cl.day}, Slot ${cl.slot} (${cl.time})</span>
                </li>
            `).join('');
        } else {
            clashBanner.classList.remove('active');
            clashItemsList.innerHTML = '';
        }

        return clashCodes;
    }

    function getClashingCourseCodes() {
        const selected = Array.from(selectedCodes).map(code => COURSES_DATA.find(c => c.code === code)).filter(Boolean);
        const clashCodes = new Set();

        for (let i = 0; i < selected.length; i++) {
            for (let j = i + 1; j < selected.length; j++) {
                const c1 = selected[i];
                const c2 = selected[j];
                if (currentExamMode === 'MID' && (c1.note === 'Only Final Exam' || c2.note === 'Only Final Exam')) {
                    continue;
                }
                if (c1.day !== 'N/A' && c1.day === c2.day && c1.slot === c2.slot) {
                    clashCodes.add(c1.code);
                    clashCodes.add(c2.code);
                }
            }
        }
        return clashCodes;
    }

    // Update Selected UI & Metrics
    function updateAppUI() {
        renderCatalog();
        renderSelectedList();
        checkClashes();
        renderTimetable();
        renderFullRoutine();
    }

    function renderSelectedList() {
        selectedListEl.innerHTML = '';
        let totalCr = 0;
        const clashCodes = getClashingCourseCodes();

        if (selectedCodes.size === 0) {
            selectedListEl.innerHTML = `
                <p style="color: var(--text-dim); font-size: 0.85rem; text-align: center; padding: 1.5rem 0;">
                    No courses selected yet.<br>Click any course checkbox to begin planning!
                </p>
            `;
        }

        selectedCodes.forEach(code => {
            const c = COURSES_DATA.find(x => x.code === code);
            if (!c) return;
            totalCr += c.cr;
            const isClash = clashCodes.has(code);

            const item = document.createElement('div');
            item.className = `selected-pill ${isClash ? 'clash-pill' : ''}`;
            item.innerHTML = `
                <div>
                    <div style="font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                        <span>${c.code}</span>
                        <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: normal;">(${c.cr} Cr)</span>
                        ${isClash ? `<span style="color: var(--danger); font-size: 0.7rem; font-weight: bold;">⚠️ CLASH</span>` : ''}
                    </div>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">${c.title}</div>
                </div>
                <button class="remove-pill-btn" onclick="toggleCourse('${c.code}')" title="Remove course">×</button>
            `;
            selectedListEl.appendChild(item);
        });

        selectedCountEl.innerText = selectedCodes.size;
        totalCreditsEl.innerText = totalCr;
        selectedCrBadge.innerText = `${totalCr} Credits`;

        // Credit Status Pill
        if (totalCr === 0) {
            creditStatusEl.innerText = 'No Courses';
            creditStatusEl.className = 'status-pill';
        } else if (totalCr < 9) {
            creditStatusEl.innerText = `Underload (${totalCr} / 9 Cr min)`;
            creditStatusEl.className = 'status-pill underload';
        } else if (totalCr <= 15) {
            creditStatusEl.innerText = `Standard Load (${totalCr} Cr)`;
            creditStatusEl.className = 'status-pill normal';
        } else {
            creditStatusEl.innerText = `Overload Warning (${totalCr} Cr)`;
            creditStatusEl.className = 'status-pill overload';
        }
    }

    // Render Weekly Timetable
    function renderTimetable() {
        timetableBody.innerHTML = '';
        const days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'];
        const slots = ['T1', 'T2', 'T3'];

        days.forEach(day => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td class="day-col">${day}</td>`;

            slots.forEach(slot => {
                const td = document.createElement('td');
                const matchingCourses = Array.from(selectedCodes)
                    .map(code => COURSES_DATA.find(x => x.code === code))
                    .filter(c => {
                        if (!c) return false;
                        if (currentExamMode === 'MID' && c.note === 'Only Final Exam') return false;
                        return c.day === day && c.slot === slot;
                    });

                if (matchingCourses.length > 0) {
                    const isClash = matchingCourses.length > 1;
                    if (isClash) {
                        td.style.background = 'rgba(239, 68, 68, 0.15)';
                    }
                    matchingCourses.forEach(c => {
                        const badge = document.createElement('span');
                        badge.className = `cell-course-badge ${isClash ? 'clash' : ''}`;
                        badge.innerText = c.code;
                        badge.title = `${c.code}: ${c.title} (${TIMINGS_DATA[currentExamMode][slot]})`;
                        td.appendChild(badge);
                    });
                } else {
                    td.innerHTML = '<span style="color: var(--text-dim); opacity: 0.3;">-</span>';
                }

                tr.appendChild(td);
            });

            timetableBody.appendChild(tr);
        });
    }

    // Advisor Lookup Feature
    function lookupAdvisor() {
        const idInput = document.getElementById('advisorStudentId');
        const program = document.getElementById('advisorProgram').value;
        const card = document.getElementById('advisorResultCard');

        const cleanIdStr = idInput.value.replace(/\\D/g, '');
        if (!cleanIdStr || cleanIdStr.length < 5) {
            card.classList.remove('active');
            return;
        }

        const idNum = parseInt(cleanIdStr, 10);
        const list = ADVISORS_DATA[program] || [];

        let found = null;
        for (const adv of list) {
            for (const r of adv.ranges) {
                if (idNum >= r[0] && idNum <= r[1]) {
                    found = adv;
                    break;
                }
            }
            if (found) break;
        }

        if (found) {
            document.getElementById('advAvatar').innerText = found.name.charAt(0);
            document.getElementById('advName').innerText = found.name;
            document.getElementById('advBatch').innerText = `${program} • ${found.batch}`;
            
            const cellEl = document.getElementById('advCell');
            cellEl.innerText = found.cell;
            cellEl.href = `tel:${found.cell}`;

            const emailEl = document.getElementById('advEmail');
            emailEl.innerText = found.email;
            emailEl.href = `mailto:${found.email}`;

            document.getElementById('advOffice').innerText = found.office;

            const rangeStrs = found.ranges.map(r => `${r[0]} - ${r[1]}`).join(' & ');
            document.getElementById('advRange').innerText = rangeStrs;

            card.classList.add('active');
        } else {
            card.classList.remove('active');
        }
    }

    // Render Full Advisor Directory
    function renderAdvisorTable() {
        const tbody = document.getElementById('advisorDirectoryBody');
        const query = (document.getElementById('advisorFilterText')?.value || '').toLowerCase();
        tbody.innerHTML = '';

        const program = document.getElementById('advisorProgram')?.value || 'BSCSE';
        const list = ADVISORS_DATA[program] || [];

        const filtered = list.filter(a => {
            if (!query) return true;
            return a.name.toLowerCase().includes(query) ||
                   a.office.toLowerCase().includes(query) ||
                   a.batch.toLowerCase().includes(query);
        });

        filtered.forEach(a => {
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--border-light)';
            tr.innerHTML = `
                <td style="padding: 0.6rem 0.8rem; font-weight: 600; color: var(--text-muted);">${a.batch}</td>
                <td style="padding: 0.6rem 0.8rem; font-weight: 700; color: var(--text-main);">${a.name}</td>
                <td style="padding: 0.6rem 0.8rem;">${a.office}</td>
                <td style="padding: 0.6rem 0.8rem;">
                    <a href="mailto:${a.email}" style="color: var(--primary); text-decoration: none; margin-right: 0.5rem;">Email</a>
                    <a href="tel:${a.cell}" style="color: var(--accent); text-decoration: none;">Call</a>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Render Full University Routine Tab
    function renderFullRoutine() {
        const grid = document.getElementById('fullRoutineGrid');
        grid.innerHTML = '';

        const days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'];
        const slots = ['T1', 'T2', 'T3'];

        days.forEach(day => {
            const dayCard = document.createElement('div');
            dayCard.className = 'routine-day-card';

            const header = document.createElement('div');
            header.className = 'routine-day-header';
            header.innerHTML = `<span>🗓️ ${day}</span> <span style="font-size: 0.75rem; color: var(--text-muted);">Mid & Final Exams</span>`;

            const slotsGrid = document.createElement('div');
            slotsGrid.className = 'routine-slots-grid';

            slots.forEach(slot => {
                const col = document.createElement('div');
                col.className = 'routine-slot-col';

                const exactTime = TIMINGS_DATA[currentExamMode][slot];
                col.innerHTML = `
                    <div class="routine-slot-title">
                        <span>Slot ${slot}</span>
                        <span style="font-family: monospace; font-size: 0.7rem; color: var(--text-muted);">${exactTime}</span>
                    </div>
                `;

                // Find all courses on this day and slot
                const slotCourses = COURSES_DATA.filter(c => c.day === day && c.slot === slot);
                slotCourses.forEach(c => {
                    const isUserSelected = selectedCodes.has(c.code);
                    const pill = document.createElement('div');
                    pill.className = `routine-course-pill ${isUserSelected ? 'is-user-selected' : ''}`;
                    pill.innerHTML = `
                        <span>${c.code} <small style="color:var(--text-dim);">${c.alt ? `(${c.alt})` : ''}</small></span>
                        <small style="font-size: 0.7rem; color: var(--text-muted);">${c.category}</small>
                    `;
                    col.appendChild(pill);
                });

                if (slotCourses.length === 0) {
                    col.innerHTML += `<span style="font-size: 0.75rem; color: var(--text-dim); padding: 0.5rem 0;">No scheduled courses</span>`;
                }

                slotsGrid.appendChild(col);
            });

            dayCard.appendChild(header);
            dayCard.appendChild(slotsGrid);
            grid.appendChild(dayCard);
        });
    }

    // Switch Primary Navigation Tab
    function switchNavTab(tab) {
        currentNavTab = tab;
        document.getElementById('viewCourses').style.display = tab === 'courses' ? 'block' : 'none';
        document.getElementById('viewAdvisor').style.display = tab === 'advisor' ? 'block' : 'none';
        document.getElementById('viewRoutine').style.display = tab === 'routine' ? 'block' : 'none';

        document.getElementById('tabCoursesBtn').classList.toggle('active', tab === 'courses');
        document.getElementById('tabAdvisorBtn').classList.toggle('active', tab === 'advisor');
        document.getElementById('tabRoutineBtn').classList.toggle('active', tab === 'routine');
    }

    // Dark / Light Theme Toggle
    function toggleTheme() {
        const body = document.body;
        const isDark = body.getAttribute('data-theme') === 'dark';
        const newTheme = isDark ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
        document.getElementById('themeIcon').innerText = isDark ? '🌙' : '☀️';
        document.getElementById('themeText').innerText = isDark ? 'Dark' : 'Light';
        localStorage.setItem('uiu_theme', newTheme);
    }

    // Reset All
    function resetSelections() {
        selectedCodes.clear();
        updateAppUI();
    }

    // Load persisted theme
    const savedTheme = localStorage.getItem('uiu_theme');
    if (savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
        document.getElementById('themeIcon').innerText = savedTheme === 'dark' ? '☀️' : '🌙';
        document.getElementById('themeText').innerText = savedTheme === 'dark' ? 'Light' : 'Dark';
    }

    init();
</script>

</body>
</html>
"""

final_html = template.replace("__COURSES_JSON__", courses_json)\
                     .replace("__ADVISORS_JSON__", advisors_json)\
                     .replace("__TIMINGS_JSON__", timings_json)

with open("d:/Exam/pre-advising.html", "w", encoding="utf-8") as f:
    f.write(final_html)

with open("d:/Exam/index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Generated pre-advising.html and index.html successfully!")
