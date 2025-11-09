#!/usr/bin/env python3
"""Update index.html with footer information"""

# Read the current HTML
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the closing </div> before </body>
footer_html = '''
        <footer style="margin-top: 60px; padding: 40px 20px; background: rgba(255,255,255,0.95); border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <!-- Important Notice -->
            <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%); border-left: 5px solid #ffc107; padding: 25px; border-radius: 15px; margin-bottom: 30px;">
                <h3 style="color: #856404; margin-bottom: 15px; font-size: 1.3em;">⚠️ Important Notice / Ważna Informacja</h3>
                
                <div style="margin-bottom: 20px;">
                    <h4 style="color: #856404; margin-bottom: 10px;">🇬🇧 English:</h4>
                    <p style="color: #856404; line-height: 1.6;">
                        This is an experimental research model for educational and testing purposes. The predictions are not absolute truth and should not be used as the sole source of verification. Always think critically, verify information from multiple reliable sources, and use your own judgment. This tool is designed to assist, not replace, human critical thinking.
                    </p>
                </div>
                
                <div>
                    <h4 style="color: #856404; margin-bottom: 10px;">🇵🇱 Polski:</h4>
                    <p style="color: #856404; line-height: 1.6;">
                        To jest eksperymentalny model badawczy do celów edukacyjnych i testowych. Predykcje nie są absolutną prawdą i nie powinny być używane jako jedyne źródło weryfikacji. Zawsze myśl krytycznie, weryfikuj informacje z wielu wiarygodnych źródeł i kieruj się własnym osądem. To narzędzie ma wspierać, a nie zastępować ludzkie myślenie krytyczne.
                    </p>
                </div>
                
                <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid rgba(133, 100, 4, 0.2); text-align: center;">
                    <p style="color: #856404; font-size: 0.95em;">
                        🧪 Test the model • Experiment with different texts • Learn about fake news patterns<br>
                        🧪 Testuj model • Eksperymentuj z różnymi tekstami • Ucz się o wzorcach fake news
                    </p>
                </div>
            </div>

            <!-- Technical Info -->
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 25px; border-radius: 15px; margin-bottom: 30px; border-left: 5px solid #2196F3;">
                <h3 style="color: #1565C0; margin-bottom: 15px; font-size: 1.2em;">🧠 Powered by Neural Network + Enhanced Pattern Detection</h3>
                <p style="color: #1565C0; margin-bottom: 10px;">
                    Real-time ML inference • Multi-language support • Hybrid AI approach
                </p>
                <div style="margin-top: 15px;">
                    <a href="https://github.com/PiotrStyla/BANED" target="_blank" style="color: #1976D2; text-decoration: none; margin-right: 15px;">📂 View on GitHub</a>
                    <a href="https://baned-xi.vercel.app/api" target="_blank" style="color: #1976D2; text-decoration: none; margin-right: 15px;">📡 API Docs</a>
                    <a href="https://www.tensorflow.org/js" target="_blank" style="color: #1976D2; text-decoration: none;">🔬 TensorFlow.js</a>
                </div>
            </div>

            <!-- Research Paper -->
            <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 25px; border-radius: 15px; margin-bottom: 30px; border-left: 5px solid #9c27b0;">
                <h3 style="color: #6a1b9a; margin-bottom: 15px; font-size: 1.1em;">📚 Based on Research</h3>
                <p style="color: #6a1b9a; font-weight: 600; margin-bottom: 8px;">
                    "Knowledge-Driven Bayesian Uncertainty Quantification for Reliable Fake News Detection"
                </p>
                <p style="color: #6a1b9a; font-size: 0.95em;">
                    Julia Puczynska, Youcef Djenouri, Michał Bizon, Tomasz Michalak and Piotr Sankowski<br>
                    <em>IDEAS NCBR Sp. z o.o.</em>
                </p>
            </div>

            <!-- Hospice Support -->
            <div style="background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%); padding: 30px; border-radius: 15px; border-left: 5px solid #e91e63;">
                <h3 style="color: #880e4f; margin-bottom: 20px; font-size: 1.3em; text-align: center;">❤️ Stworzone z sercem dla Fundacji Hospicjum</h3>
                
                <p style="color: #880e4f; text-align: center; margin-bottom: 20px; font-size: 1.05em; line-height: 1.6;">
                    Ta aplikacja jest całkowicie <strong>bezpłatna</strong> i zawsze taka pozostanie.<br>
                    Jeśli chcesz wesprzeć rozwój aplikacji i działania Fundacji,<br>
                    możesz przekazać dobrowolną darowiznę wspierającą <strong>Hospicjum Maryi Królowej Apostołów w Krakowie</strong>.
                </p>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h4 style="color: #880e4f; margin-bottom: 15px; text-align: center;">💳 Numer konta (Działalność statutowa):</h4>
                    <p style="color: #880e4f; font-size: 1.2em; font-weight: bold; text-align: center; font-family: monospace; letter-spacing: 1px;">
                        50 1870 1045 2078 1079 2447 0001
                    </p>
                    <p style="color: #880e4f; text-align: center; margin-top: 10px; font-size: 0.9em;">
                        SWIFT: NESBPLPW
                    </p>
                    <p style="color: #880e4f; text-align: center; margin-top: 15px; font-size: 0.85em;">
                        KRS: 0001063161 | NIP: 6793279476 | REGON: 526664276
                    </p>
                </div>
                
                <div style="text-align: center; margin-top: 25px;">
                    <a href="https://fundacjahospicjum.pl" target="_blank" style="display: inline-block; background: #e91e63; color: white; padding: 15px 30px; border-radius: 25px; text-decoration: none; font-weight: 600; margin: 5px; transition: transform 0.2s;">
                        💝 Wspieraj Fundację
                    </a>
                    <a href="https://fundacjahospicjum.pl/hospicjum" target="_blank" style="display: inline-block; background: #880e4f; color: white; padding: 15px 30px; border-radius: 25px; text-decoration: none; font-weight: 600; margin: 5px; transition: transform 0.2s;">
                        🏥 Hospicjum w Krakowie
                    </a>
                </div>
                
                <div style="margin-top: 25px; padding-top: 20px; border-top: 2px solid rgba(136, 14, 79, 0.2);">
                    <p style="color: #880e4f; text-align: center; font-size: 0.95em; line-height: 1.8;">
                        W ramach działalności Fundacji prowadzone są:<br>
                        🦋 <strong>Gabinety Papilio</strong> • 🎨 <strong>Kraftownia</strong> • 🛍️ <strong>Sklep Kraftowni</strong>
                    </p>
                    <p style="color: #880e4f; text-align: center; margin-top: 15px; font-size: 0.9em; font-style: italic;">
                        Wszystkie działania prowadzone są w celu wsparcia Hospicjum Maryi Królowej Apostołów w Krakowie
                    </p>
                </div>
            </div>

            <!-- Copyright -->
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd;">
                <p style="color: #666; font-size: 0.9em;">
                    © 2025 BANED Double Power • Made with ❤️ for education and research
                </p>
            </div>
        </footer>
    </div>
</body>
</html>'''

# Replace the closing tags
html = html.replace('    </div>\n</body>\n</html>', footer_html)

# Write the updated HTML
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Footer added successfully!")
print("   - Important notice (EN/PL)")
print("   - Technical info with links")
print("   - Research paper credits")
print("   - Hospice donation information")
print("   - Foundation activities")
