"""Verify the original form behavior; no WhatsApp message is sent."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':900})
 page.goto('http://localhost:3000/',wait_until='networkidle')
 assert page.locator('#ski-request-form').is_visible()
 page.locator('select[name="experience"]').select_option('Performance & technique')
 page.wait_for_function("document.querySelector('select[name=participants]').options[2].disabled")
 assert page.locator('select[name="participants"]').input_value()=='1 personne'
 page.locator('select[name="experience"]').select_option('Leçons particulières')
 assert not page.evaluate("document.querySelector('select[name=participants]').options[2].disabled")
 assert page.locator('select[name="format"] option',has_text='Demi-journée').is_enabled()
 page.locator('select[name="format"]').select_option('Demi-journée')
 page.locator('select[name="experience"]').select_option('Freeride & milieu alpin')
 page.wait_for_function("document.querySelector('select[name=format]').options[1].disabled")
 assert page.locator('select[name="format"]').input_value()=='Journée'
 print('PASS: original visible form and selection behavior restored; no message sent.')
 browser.close()
