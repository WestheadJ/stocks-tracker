import os
from menu import Menu
from db.db_setup import setup_db
from file_browser import file_browser
from report_importer.import_file import start_import
from console_manager import log
from reports_display import window


# --- Menu Callbacks ---
def start_reports():
    from reports_browser import reports_browser

    selected = reports_browser()
    if selected == "ESC":
        log("[INFO] No report selected. Returning to menu...")
    elif selected:
        window.open_report(
            selected["current_year"], selected["current_month"], selected["breakdown"]
        )

    else:
        exit(0)


def import_report():
    #  Get file
    file = file_browser()
    if file == "ESC":
        log("[INFO] No file selected. Returning to menu...")
    # Use file
    elif file:
        # Start the process
        start_import(file)
        #
        # with ImportFile(file) as importer:
        #     log(f"Till: {importer.till}")
        #     log(f"Start: {importer.start_date}")
        #     log(f"End: {importer.end_date}")
        #     log(f"Period: {importer.period}")
        #     save_import(importer)


def start_products():
    log("🛠 Products menu coming soon...")


def start_configuration():
    log("⚙️ Configuration menu coming soon...")


def start_advanced():
    log("📂 Advanced DB explorer coming soon...")


# --- Menu Options ---
menu_options = [
    ("Reports", start_reports),
    ("Import Report", import_report),
    ("Products", start_products),
    ("Configuration", start_configuration),
    ("Advanced", start_advanced),
    ("Exit", lambda: exit(0)),
]


# --- Main Entry Point ---
def main():
    if not os.path.isfile("sales_tracker.duckdb"):
        setup_db()

    main_menu = Menu("📊 Product Sales Tracker", menu_options)
    main_menu.run()


if __name__ == "__main__":
    main()
