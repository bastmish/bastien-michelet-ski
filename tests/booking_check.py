"""Inspect booking choices without sending a message."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':900})
 page.goto('http://localhost:3000/',wait_until='networkidle')
 page.locator('select[name="format"]').select_option('Demi-journée')
 page.locator('select[name="experience"]').select_option('Freeride & milieu alpin')
 assert page.evaluate("document.querySelector('select[name=format]').options[1].disabled")
 assert page.locator('select[name="format"]').input_value()=='Journée'
 page.locator('select[name="experience"]').select_option('Performance & technique')
 assert not page.evaluate("document.querySelector('select[name=format]').options[1].disabled")
 assert page.locator('select[name="participants"] option',has_text='2 personnes').is_enabled()
 print('PASS: freeride half-day excluded, existing selection corrected, coaching enquiry remains open.')
 browser.close()
