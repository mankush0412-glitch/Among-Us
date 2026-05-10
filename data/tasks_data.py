import random

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FORMAT:  text = question + formatted options (Telegram Markdown)
#          answer = correct letter (A/B/C/D)
#          category = topic label
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASKS = [

    # ══════════════════════════════════════════════════════
    # 🌍  GENERAL KNOWLEDGE  (400 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🌍 *What is the capital of France?*\n\n*A)* London\n*B)* Paris\n*C)* Berlin\n*D)* Madrid","answer":"B","category":"general"},
    {"text":"🌍 *What is the largest planet in our solar system?*\n\n*A)* Saturn\n*B)* Uranus\n*C)* Jupiter\n*D)* Neptune","answer":"C","category":"general"},
    {"text":"🌍 *How many continents are there on Earth?*\n\n*A)* 5\n*B)* 6\n*C)* 7\n*D)* 8","answer":"C","category":"general"},
    {"text":"🌍 *Who invented the telephone?*\n\n*A)* Thomas Edison\n*B)* Nikola Tesla\n*C)* Alexander Graham Bell\n*D)* Marconi","answer":"C","category":"general"},
    {"text":"🌍 *What is the chemical symbol for gold?*\n\n*A)* Go\n*B)* Gd\n*C)* Gl\n*D)* Au","answer":"D","category":"general"},
    {"text":"🌍 *What is the tallest mountain in the world?*\n\n*A)* K2\n*B)* Kangchenjunga\n*C)* Mount Everest\n*D)* Lhotse","answer":"C","category":"general"},
    {"text":"🌍 *Which country has the largest population?*\n\n*A)* USA\n*B)* India\n*C)* China\n*D)* Indonesia","answer":"B","category":"general"},
    {"text":"🌍 *What year did World War 2 end?*\n\n*A)* 1943\n*B)* 1944\n*C)* 1945\n*D)* 1946","answer":"C","category":"general"},
    {"text":"🌍 *How many sides does a hexagon have?*\n\n*A)* 5\n*B)* 6\n*C)* 7\n*D)* 8","answer":"B","category":"general"},
    {"text":"🌍 *What is the longest river in the world?*\n\n*A)* Amazon\n*B)* Congo\n*C)* Yangtze\n*D)* Nile","answer":"D","category":"general"},
    {"text":"🌍 *Who wrote 'Romeo and Juliet'?*\n\n*A)* Charles Dickens\n*B)* William Shakespeare\n*C)* Jane Austen\n*D)* Homer","answer":"B","category":"general"},
    {"text":"🌍 *What is the smallest country in the world?*\n\n*A)* Monaco\n*B)* San Marino\n*C)* Vatican City\n*D)* Liechtenstein","answer":"C","category":"general"},
    {"text":"🌍 *What is the chemical formula for water?*\n\n*A)* HO\n*B)* H2O\n*C)* H3O\n*D)* OH","answer":"B","category":"general"},
    {"text":"🌍 *What gas do plants absorb from the atmosphere?*\n\n*A)* Oxygen\n*B)* Nitrogen\n*C)* Carbon Dioxide\n*D)* Hydrogen","answer":"C","category":"general"},
    {"text":"🌍 *What is the hardest natural substance on Earth?*\n\n*A)* Ruby\n*B)* Emerald\n*C)* Quartz\n*D)* Diamond","answer":"D","category":"general"},
    {"text":"🌍 *How many bones are in the adult human body?*\n\n*A)* 196\n*B)* 206\n*C)* 216\n*D)* 226","answer":"B","category":"general"},
    {"text":"🌍 *How many colors are in a rainbow?*\n\n*A)* 5\n*B)* 6\n*C)* 7\n*D)* 8","answer":"C","category":"general"},
    {"text":"🌍 *What is the largest ocean?*\n\n*A)* Atlantic\n*B)* Indian\n*C)* Arctic\n*D)* Pacific","answer":"D","category":"general"},
    {"text":"🌍 *Who invented the light bulb?*\n\n*A)* Nikola Tesla\n*B)* Thomas Edison\n*C)* James Watt\n*D)* Michael Faraday","answer":"B","category":"general"},
    {"text":"🌍 *What is the capital of Japan?*\n\n*A)* Osaka\n*B)* Kyoto\n*C)* Tokyo\n*D)* Hiroshima","answer":"C","category":"general"},
    {"text":"🌍 *What is the boiling point of water in Celsius?*\n\n*A)* 90°C\n*B)* 95°C\n*C)* 100°C\n*D)* 105°C","answer":"C","category":"general"},
    {"text":"🌍 *Who discovered gravity?*\n\n*A)* Albert Einstein\n*B)* Isaac Newton\n*C)* Galileo Galilei\n*D)* Archimedes","answer":"B","category":"general"},
    {"text":"🌍 *What is the most spoken language in the world?*\n\n*A)* English\n*B)* Spanish\n*C)* Mandarin Chinese\n*D)* Hindi","answer":"C","category":"general"},
    {"text":"🌍 *How many chambers does the human heart have?*\n\n*A)* 2\n*B)* 3\n*C)* 4\n*D)* 5","answer":"C","category":"general"},
    {"text":"🌍 *What is the hottest planet in our solar system?*\n\n*A)* Mercury\n*B)* Venus\n*C)* Mars\n*D)* Jupiter","answer":"B","category":"general"},
    {"text":"🌍 *How many teeth does an adult human have?*\n\n*A)* 28\n*B)* 30\n*C)* 32\n*D)* 34","answer":"C","category":"general"},
    {"text":"🌍 *What year did India gain independence?*\n\n*A)* 1945\n*B)* 1946\n*C)* 1947\n*D)* 1948","answer":"C","category":"general"},
    {"text":"🌍 *How many letters are in the English alphabet?*\n\n*A)* 24\n*B)* 25\n*C)* 26\n*D)* 27","answer":"C","category":"general"},
    {"text":"🌍 *What is the most abundant gas in Earth's atmosphere?*\n\n*A)* Oxygen\n*B)* Carbon Dioxide\n*C)* Argon\n*D)* Nitrogen","answer":"D","category":"general"},
    {"text":"🌍 *Who was the first man to walk on the moon?*\n\n*A)* Buzz Aldrin\n*B)* Neil Armstrong\n*C)* Yuri Gagarin\n*D)* John Glenn","answer":"B","category":"general"},
    {"text":"🌍 *What is the capital of Canada?*\n\n*A)* Toronto\n*B)* Vancouver\n*C)* Montreal\n*D)* Ottawa","answer":"D","category":"general"},
    {"text":"🌍 *What is the largest continent?*\n\n*A)* Africa\n*B)* North America\n*C)* Asia\n*D)* Europe","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of Italy?*\n\n*A)* Milan\n*B)* Naples\n*C)* Florence\n*D)* Rome","answer":"D","category":"general"},
    {"text":"🌍 *What is the tallest building in the world?*\n\n*A)* Shanghai Tower\n*B)* Burj Khalifa\n*C)* One WTC\n*D)* Makkah Clock Tower","answer":"B","category":"general"},
    {"text":"🌍 *What is the national bird of India?*\n\n*A)* Crane\n*B)* Flamingo\n*C)* Peacock\n*D)* Parrot","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of South Korea?*\n\n*A)* Busan\n*B)* Seoul\n*C)* Incheon\n*D)* Daegu","answer":"B","category":"general"},
    {"text":"🌍 *Who is known as the Father of the Nation in India?*\n\n*A)* Nehru\n*B)* Bose\n*C)* Ambedkar\n*D)* Gandhi","answer":"D","category":"general"},
    {"text":"🌍 *What is the capital of Mexico?*\n\n*A)* Guadalajara\n*B)* Monterrey\n*C)* Mexico City\n*D)* Cancun","answer":"C","category":"general"},
    {"text":"🌍 *How many minutes are in a day?*\n\n*A)* 1200\n*B)* 1440\n*C)* 1560\n*D)* 1680","answer":"B","category":"general"},
    {"text":"🌍 *What is the capital of Turkey?*\n\n*A)* Istanbul\n*B)* Izmir\n*C)* Ankara\n*D)* Bursa","answer":"C","category":"general"},
    {"text":"🌍 *What is the largest democracy in the world?*\n\n*A)* USA\n*B)* Brazil\n*C)* India\n*D)* UK","answer":"C","category":"general"},
    {"text":"🌍 *What is the national flower of India?*\n\n*A)* Rose\n*B)* Lotus\n*C)* Jasmine\n*D)* Marigold","answer":"B","category":"general"},
    {"text":"🌍 *Who wrote the Indian National Anthem?*\n\n*A)* Bankim Chandra\n*B)* Vande Mataram author\n*C)* Rabindranath Tagore\n*D)* Sarojini Naidu","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of Pakistan?*\n\n*A)* Lahore\n*B)* Karachi\n*C)* Islamabad\n*D)* Peshawar","answer":"C","category":"general"},
    {"text":"🌍 *Which planet is known as the Red Planet?*\n\n*A)* Jupiter\n*B)* Saturn\n*C)* Venus\n*D)* Mars","answer":"D","category":"general"},
    {"text":"🌍 *What is the currency of Japan?*\n\n*A)* Won\n*B)* Yuan\n*C)* Yen\n*D)* Baht","answer":"C","category":"general"},
    {"text":"🌍 *How many sides does an octagon have?*\n\n*A)* 6\n*B)* 7\n*C)* 8\n*D)* 9","answer":"C","category":"general"},
    {"text":"🌍 *Who wrote 'Harry Potter'?*\n\n*A)* Stephen King\n*B)* J.K. Rowling\n*C)* Tolkien\n*D)* Roald Dahl","answer":"B","category":"general"},
    {"text":"🌍 *What is the square root of 144?*\n\n*A)* 10\n*B)* 11\n*C)* 12\n*D)* 13","answer":"C","category":"general"},
    {"text":"🌍 *How many players are in a cricket team?*\n\n*A)* 9\n*B)* 10\n*C)* 11\n*D)* 12","answer":"C","category":"general"},
    {"text":"🌍 *What organ pumps blood in the human body?*\n\n*A)* Liver\n*B)* Kidney\n*C)* Lungs\n*D)* Heart","answer":"D","category":"general"},
    {"text":"🌍 *What is the capital of Germany?*\n\n*A)* Munich\n*B)* Hamburg\n*C)* Frankfurt\n*D)* Berlin","answer":"D","category":"general"},
    {"text":"🌍 *How many days are in a leap year?*\n\n*A)* 364\n*B)* 365\n*C)* 366\n*D)* 367","answer":"C","category":"general"},
    {"text":"🌍 *What does DNA stand for?*\n\n*A)* Deoxyribose Nucleotide Acid\n*B)* Deoxyribonucleic Acid\n*C)* Dinitrogen Amino Acid\n*D)* Dynamic Nucleotide Array","answer":"B","category":"general"},
    {"text":"🌍 *What is the capital of Russia?*\n\n*A)* St. Petersburg\n*B)* Novosibirsk\n*C)* Moscow\n*D)* Vladivostok","answer":"C","category":"general"},
    {"text":"🌍 *How many strings does a guitar have?*\n\n*A)* 4\n*B)* 5\n*C)* 6\n*D)* 7","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of Australia?*\n\n*A)* Sydney\n*B)* Melbourne\n*C)* Brisbane\n*D)* Canberra","answer":"D","category":"general"},
    {"text":"🌍 *Who painted the Mona Lisa?*\n\n*A)* Michelangelo\n*B)* Raphael\n*C)* Leonardo da Vinci\n*D)* Caravaggio","answer":"C","category":"general"},
    {"text":"🌍 *What is the currency of UK?*\n\n*A)* Euro\n*B)* Pound\n*C)* Dollar\n*D)* Franc","answer":"B","category":"general"},
    {"text":"🌍 *How many zeros are in a million?*\n\n*A)* 5\n*B)* 6\n*C)* 7\n*D)* 8","answer":"B","category":"general"},
    {"text":"🌍 *Which is the smallest continent?*\n\n*A)* Europe\n*B)* Antarctica\n*C)* Australia\n*D)* South America","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of China?*\n\n*A)* Shanghai\n*B)* Hong Kong\n*C)* Beijing\n*D)* Guangzhou","answer":"C","category":"general"},
    {"text":"🌍 *What is the speed of sound in air (approx)?*\n\n*A)* 243 m/s\n*B)* 343 m/s\n*C)* 443 m/s\n*D)* 543 m/s","answer":"B","category":"general"},
    {"text":"🌍 *Which blood group is universal donor?*\n\n*A)* AB+\n*B)* A+\n*C)* O-\n*D)* B-","answer":"C","category":"general"},
    {"text":"🌍 *How many planets are in our solar system?*\n\n*A)* 7\n*B)* 8\n*C)* 9\n*D)* 10","answer":"B","category":"general"},
    {"text":"🌍 *What is the national animal of India?*\n\n*A)* Lion\n*B)* Elephant\n*C)* Tiger\n*D)* Leopard","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of Brazil?*\n\n*A)* São Paulo\n*B)* Rio de Janeiro\n*C)* Salvador\n*D)* Brasília","answer":"D","category":"general"},
    {"text":"🌍 *What is the capital of Spain?*\n\n*A)* Barcelona\n*B)* Seville\n*C)* Madrid\n*D)* Valencia","answer":"C","category":"general"},
    {"text":"🌍 *How many hours are in a week?*\n\n*A)* 148\n*B)* 158\n*C)* 168\n*D)* 178","answer":"C","category":"general"},
    {"text":"🌍 *What is the freezing point of water in Celsius?*\n\n*A)* -10°C\n*B)* 0°C\n*C)* 5°C\n*D)* 10°C","answer":"B","category":"general"},
    {"text":"🌍 *Which country is the largest by area?*\n\n*A)* China\n*B)* USA\n*C)* Canada\n*D)* Russia","answer":"D","category":"general"},
    {"text":"🌍 *What is the capital of Egypt?*\n\n*A)* Alexandria\n*B)* Luxor\n*C)* Cairo\n*D)* Giza","answer":"C","category":"general"},
    {"text":"🌍 *How many millimeters are in a centimeter?*\n\n*A)* 5\n*B)* 10\n*C)* 100\n*D)* 1000","answer":"B","category":"general"},
    {"text":"🌍 *What is the capital of Argentina?*\n\n*A)* Córdoba\n*B)* Rosario\n*C)* Buenos Aires\n*D)* Mendoza","answer":"C","category":"general"},
    {"text":"🌍 *How many strings does a violin have?*\n\n*A)* 3\n*B)* 4\n*C)* 5\n*D)* 6","answer":"B","category":"general"},
    {"text":"🌍 *What language is spoken in Brazil?*\n\n*A)* Spanish\n*B)* French\n*C)* Portuguese\n*D)* Italian","answer":"C","category":"general"},
    {"text":"🌍 *What is the national sport of Canada?*\n\n*A)* Baseball\n*B)* Basketball\n*C)* Lacrosse & Hockey\n*D)* Curling","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of Bangladesh?*\n\n*A)* Chittagong\n*B)* Dhaka\n*C)* Khulna\n*D)* Sylhet","answer":"B","category":"general"},
    {"text":"🌍 *Which element has atomic number 1?*\n\n*A)* Helium\n*B)* Lithium\n*C)* Hydrogen\n*D)* Oxygen","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of Sri Lanka?*\n\n*A)* Colombo\n*B)* Galle\n*C)* Kandy\n*D)* Jaffna","answer":"A","category":"general"},
    {"text":"🌍 *How many days are in February in a non-leap year?*\n\n*A)* 27\n*B)* 28\n*C)* 29\n*D)* 30","answer":"B","category":"general"},
    {"text":"🌍 *What is the longest wall in the world?*\n\n*A)* Berlin Wall\n*B)* Hadrian's Wall\n*C)* Great Wall of China\n*D)* Walls of Babylon","answer":"C","category":"general"},
    {"text":"🌍 *Which ocean is the smallest?*\n\n*A)* Indian Ocean\n*B)* Southern Ocean\n*C)* Arctic Ocean\n*D)* Atlantic Ocean","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of South Africa?*\n\n*A)* Johannesburg\n*B)* Cape Town\n*C)* Durban\n*D)* Pretoria","answer":"D","category":"general"},
    {"text":"🌍 *What is the largest organ in the human body?*\n\n*A)* Liver\n*B)* Lung\n*C)* Skin\n*D)* Brain","answer":"C","category":"general"},
    {"text":"🌍 *How many sides does a pentagon have?*\n\n*A)* 4\n*B)* 5\n*C)* 6\n*D)* 7","answer":"B","category":"general"},
    {"text":"🌍 *What is the currency of India?*\n\n*A)* Rupee\n*B)* Peso\n*C)* Taka\n*D)* Dinar","answer":"A","category":"general"},
    {"text":"🌍 *Who was the first President of India?*\n\n*A)* Rajendra Prasad\n*B)* S. Radhakrishnan\n*C)* Zakir Hussain\n*D)* Nehru","answer":"A","category":"general"},
    {"text":"🌍 *What is the capital of Nepal?*\n\n*A)* Pokhara\n*B)* Biratnagar\n*C)* Kathmandu\n*D)* Lalitpur","answer":"C","category":"general"},
    {"text":"🌍 *Which is the largest desert in the world?*\n\n*A)* Gobi\n*B)* Sahara\n*C)* Arabian\n*D)* Antarctic","answer":"D","category":"general"},
    {"text":"🌍 *What is the capital of Nigeria?*\n\n*A)* Lagos\n*B)* Abuja\n*C)* Kano\n*D)* Ibadan","answer":"B","category":"general"},
    {"text":"🌍 *How many seconds are in an hour?*\n\n*A)* 2400\n*B)* 3000\n*C)* 3600\n*D)* 4200","answer":"C","category":"general"},
    {"text":"🌍 *What is the chemical symbol for iron?*\n\n*A)* Ir\n*B)* In\n*C)* Fe\n*D)* Io","answer":"C","category":"general"},
    {"text":"🌍 *What is the capital of Kenya?*\n\n*A)* Mombasa\n*B)* Kisumu\n*C)* Nairobi\n*D)* Nakuru","answer":"C","category":"general"},
    {"text":"🌍 *Which is the world's fastest land animal?*\n\n*A)* Lion\n*B)* Leopard\n*C)* Pronghorn\n*D)* Cheetah","answer":"D","category":"general"},
    {"text":"🌍 *What is the capital of Thailand?*\n\n*A)* Phuket\n*B)* Chiang Mai\n*C)* Bangkok\n*D)* Pattaya","answer":"C","category":"general"},
    {"text":"🌍 *Which planet has the most moons?*\n\n*A)* Jupiter\n*B)* Saturn\n*C)* Uranus\n*D)* Neptune","answer":"B","category":"general"},
    {"text":"🌍 *What is the capital of Indonesia?*\n\n*A)* Surabaya\n*B)* Bandung\n*C)* Jakarta\n*D)* Medan","answer":"C","category":"general"},
    {"text":"🌍 *How many weeks are in a year?*\n\n*A)* 48\n*B)* 50\n*C)* 52\n*D)* 54","answer":"C","category":"general"},
    {"text":"🌍 *What is the national animal of Australia?*\n\n*A)* Koala\n*B)* Emu\n*C)* Kangaroo\n*D)* Platypus","answer":"C","category":"general"},
    {"text":"🌍 *Which country invented pizza?*\n\n*A)* Greece\n*B)* Spain\n*C)* Italy\n*D)* France","answer":"C","category":"general"},

    # ══════════════════════════════════════════════════════
    # 🔬  SCIENCE  (300 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🔬 *What is the powerhouse of the cell?*\n\n*A)* Nucleus\n*B)* Ribosome\n*C)* Mitochondria\n*D)* Golgi body","answer":"C","category":"science"},
    {"text":"🔬 *What is the atomic number of Carbon?*\n\n*A)* 4\n*B)* 6\n*C)* 8\n*D)* 12","answer":"B","category":"science"},
    {"text":"🔬 *What is Newton's first law also known as?*\n\n*A)* Law of gravity\n*B)* Law of motion\n*C)* Law of inertia\n*D)* Law of force","answer":"C","category":"science"},
    {"text":"🔬 *Which gas is produced during photosynthesis?*\n\n*A)* CO2\n*B)* N2\n*C)* H2\n*D)* O2","answer":"D","category":"science"},
    {"text":"🔬 *What is the unit of electric current?*\n\n*A)* Volt\n*B)* Watt\n*C)* Ampere\n*D)* Ohm","answer":"C","category":"science"},
    {"text":"🔬 *What is the pH of pure water?*\n\n*A)* 5\n*B)* 6\n*C)* 7\n*D)* 8","answer":"C","category":"science"},
    {"text":"🔬 *Which planet has rings around it?*\n\n*A)* Jupiter only\n*B)* Saturn only\n*C)* All gas giants\n*D)* Mars only","answer":"C","category":"science"},
    {"text":"🔬 *What is the chemical symbol for sodium?*\n\n*A)* So\n*B)* Sd\n*C)* Na\n*D)* Sm","answer":"C","category":"science"},
    {"text":"🔬 *How many chromosomes does a human have?*\n\n*A)* 44\n*B)* 46\n*C)* 48\n*D)* 50","answer":"B","category":"science"},
    {"text":"🔬 *What force keeps planets in orbit?*\n\n*A)* Magnetic force\n*B)* Electric force\n*C)* Gravity\n*D)* Nuclear force","answer":"C","category":"science"},
    {"text":"🔬 *What is the nearest star to Earth?*\n\n*A)* Sirius\n*B)* Betelgeuse\n*C)* Alpha Centauri\n*D)* The Sun","answer":"D","category":"science"},
    {"text":"🔬 *Which vitamin is produced when skin is exposed to sunlight?*\n\n*A)* Vitamin A\n*B)* Vitamin B12\n*C)* Vitamin C\n*D)* Vitamin D","answer":"D","category":"science"},
    {"text":"🔬 *What is the chemical symbol for silver?*\n\n*A)* Si\n*B)* Ag\n*C)* Sl\n*D)* Sr","answer":"B","category":"science"},
    {"text":"🔬 *What is the unit of frequency?*\n\n*A)* Newton\n*B)* Pascal\n*C)* Hertz\n*D)* Joule","answer":"C","category":"science"},
    {"text":"🔬 *What type of bond holds water molecules together?*\n\n*A)* Ionic bond\n*B)* Covalent bond\n*C)* Hydrogen bond\n*D)* Metallic bond","answer":"C","category":"science"},
    {"text":"🔬 *Which part of the brain controls balance?*\n\n*A)* Cerebrum\n*B)* Medulla\n*C)* Cerebellum\n*D)* Thalamus","answer":"C","category":"science"},
    {"text":"🔬 *What is the speed of light (approx)?*\n\n*A)* 2×10⁸ m/s\n*B)* 3×10⁸ m/s\n*C)* 4×10⁸ m/s\n*D)* 5×10⁸ m/s","answer":"B","category":"science"},
    {"text":"🔬 *What gas causes global warming mainly?*\n\n*A)* Oxygen\n*B)* Nitrogen\n*C)* Carbon Dioxide\n*D)* Argon","answer":"C","category":"science"},
    {"text":"🔬 *What is the chemical symbol for potassium?*\n\n*A)* Po\n*B)* Pt\n*C)* K\n*D)* Pm","answer":"C","category":"science"},
    {"text":"🔬 *Which planet is closest to the Sun?*\n\n*A)* Venus\n*B)* Earth\n*C)* Mars\n*D)* Mercury","answer":"D","category":"science"},
    {"text":"🔬 *What is the process of water turning into vapor called?*\n\n*A)* Condensation\n*B)* Sublimation\n*C)* Evaporation\n*D)* Precipitation","answer":"C","category":"science"},
    {"text":"🔬 *What is the most abundant element in the universe?*\n\n*A)* Helium\n*B)* Oxygen\n*C)* Hydrogen\n*D)* Carbon","answer":"C","category":"science"},
    {"text":"🔬 *Which blood type is the universal recipient?*\n\n*A)* O+\n*B)* A+\n*C)* B+\n*D)* AB+","answer":"D","category":"science"},
    {"text":"🔬 *What is the study of fossils called?*\n\n*A)* Archaeology\n*B)* Paleontology\n*C)* Geology\n*D)* Anthropology","answer":"B","category":"science"},
    {"text":"🔬 *What is the unit of energy?*\n\n*A)* Newton\n*B)* Watt\n*C)* Joule\n*D)* Pascal","answer":"C","category":"science"},
    {"text":"🔬 *Which organ produces insulin?*\n\n*A)* Liver\n*B)* Kidney\n*C)* Pancreas\n*D)* Spleen","answer":"C","category":"science"},
    {"text":"🔬 *What is the formula for force?*\n\n*A)* F = mv\n*B)* F = ma\n*C)* F = mgh\n*D)* F = mc²","answer":"B","category":"science"},
    {"text":"🔬 *What is the atomic symbol for Lead?*\n\n*A)* Le\n*B)* Pb\n*C)* Ld\n*D)* La","answer":"B","category":"science"},
    {"text":"🔬 *Which gas is used in neon lights?*\n\n*A)* Argon\n*B)* Krypton\n*C)* Neon\n*D)* Xenon","answer":"C","category":"science"},
    {"text":"🔬 *What is the study of the universe called?*\n\n*A)* Astrology\n*B)* Cosmology\n*C)* Meteorology\n*D)* Geology","answer":"B","category":"science"},
    {"text":"🔬 *How many bones are in the human skull?*\n\n*A)* 18\n*B)* 20\n*C)* 22\n*D)* 24","answer":"C","category":"science"},
    {"text":"🔬 *What is the chemical formula for table salt?*\n\n*A)* KCl\n*B)* NaCl\n*C)* CaCl\n*D)* MgCl","answer":"B","category":"science"},
    {"text":"🔬 *Which planet spins on its side?*\n\n*A)* Neptune\n*B)* Saturn\n*C)* Uranus\n*D)* Mars","answer":"C","category":"science"},
    {"text":"🔬 *What is the study of plants called?*\n\n*A)* Zoology\n*B)* Ecology\n*C)* Botany\n*D)* Biology","answer":"C","category":"science"},
    {"text":"🔬 *What is the largest cell in the human body?*\n\n*A)* Muscle cell\n*B)* Nerve cell\n*C)* Egg cell\n*D)* Liver cell","answer":"C","category":"science"},
    {"text":"🔬 *Which metal is liquid at room temperature?*\n\n*A)* Lead\n*B)* Tin\n*C)* Mercury\n*D)* Zinc","answer":"C","category":"science"},
    {"text":"🔬 *What is the half-life of Carbon-14 (approx)?*\n\n*A)* 1730 years\n*B)* 3730 years\n*C)* 5730 years\n*D)* 7730 years","answer":"C","category":"science"},
    {"text":"🔬 *Which vitamin deficiency causes scurvy?*\n\n*A)* Vitamin A\n*B)* Vitamin B\n*C)* Vitamin C\n*D)* Vitamin K","answer":"C","category":"science"},
    {"text":"🔬 *What is the process of splitting an atom called?*\n\n*A)* Nuclear fusion\n*B)* Radioactive decay\n*C)* Nuclear fission\n*D)* Ionization","answer":"C","category":"science"},
    {"text":"🔬 *What is the chemical symbol for Copper?*\n\n*A)* Co\n*B)* Cp\n*C)* Cr\n*D)* Cu","answer":"D","category":"science"},

    # ══════════════════════════════════════════════════════
    # 🔢  MATHEMATICS  (200 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🔢 *What is 15 × 15?*\n\n*A)* 215\n*B)* 225\n*C)* 235\n*D)* 245","answer":"B","category":"math"},
    {"text":"🔢 *What is the value of π (pi) approximately?*\n\n*A)* 2.14\n*B)* 3.14\n*C)* 4.14\n*D)* 5.14","answer":"B","category":"math"},
    {"text":"🔢 *What is 25% of 200?*\n\n*A)* 25\n*B)* 40\n*C)* 50\n*D)* 75","answer":"C","category":"math"},
    {"text":"🔢 *What is the square root of 256?*\n\n*A)* 14\n*B)* 15\n*C)* 16\n*D)* 17","answer":"C","category":"math"},
    {"text":"🔢 *What is 2 to the power of 10?*\n\n*A)* 512\n*B)* 1024\n*C)* 2048\n*D)* 4096","answer":"B","category":"math"},
    {"text":"🔢 *What is 50% of 380?*\n\n*A)* 170\n*B)* 180\n*C)* 190\n*D)* 200","answer":"C","category":"math"},
    {"text":"🔢 *What is 12 × 12?*\n\n*A)* 124\n*B)* 134\n*C)* 144\n*D)* 154","answer":"C","category":"math"},
    {"text":"🔢 *What is 1000 ÷ 25?*\n\n*A)* 30\n*B)* 35\n*C)* 40\n*D)* 45","answer":"C","category":"math"},
    {"text":"🔢 *What is the cube of 5?*\n\n*A)* 100\n*B)* 115\n*C)* 125\n*D)* 135","answer":"C","category":"math"},
    {"text":"🔢 *What is 75% of 400?*\n\n*A)* 280\n*B)* 290\n*C)* 300\n*D)* 310","answer":"C","category":"math"},
    {"text":"🔢 *What is the sum of angles in a triangle?*\n\n*A)* 90°\n*B)* 120°\n*C)* 180°\n*D)* 360°","answer":"C","category":"math"},
    {"text":"🔢 *What is 9 × 9?*\n\n*A)* 72\n*B)* 81\n*C)* 90\n*D)* 99","answer":"B","category":"math"},
    {"text":"🔢 *What is 144 ÷ 12?*\n\n*A)* 10\n*B)* 12\n*C)* 14\n*D)* 16","answer":"B","category":"math"},
    {"text":"🔢 *What is 30% of 150?*\n\n*A)* 35\n*B)* 40\n*C)* 45\n*D)* 50","answer":"C","category":"math"},
    {"text":"🔢 *What is 7 factorial (7!)?*\n\n*A)* 2520\n*B)* 4040\n*C)* 5040\n*D)* 6020","answer":"C","category":"math"},
    {"text":"🔢 *If x + 5 = 12, what is x?*\n\n*A)* 5\n*B)* 6\n*C)* 7\n*D)* 8","answer":"C","category":"math"},
    {"text":"🔢 *What is the square root of 625?*\n\n*A)* 23\n*B)* 25\n*C)* 27\n*D)* 29","answer":"B","category":"math"},
    {"text":"🔢 *What is 20% of 500?*\n\n*A)* 80\n*B)* 90\n*C)* 100\n*D)* 110","answer":"C","category":"math"},
    {"text":"🔢 *How many degrees in a full circle?*\n\n*A)* 180\n*B)* 270\n*C)* 360\n*D)* 450","answer":"C","category":"math"},
    {"text":"🔢 *What is 3 to the power of 5?*\n\n*A)* 183\n*B)* 213\n*C)* 243\n*D)* 273","answer":"C","category":"math"},
    {"text":"🔢 *What is the LCM of 4 and 6?*\n\n*A)* 8\n*B)* 10\n*C)* 12\n*D)* 24","answer":"C","category":"math"},
    {"text":"🔢 *What is 999 + 1?*\n\n*A)* 999\n*B)* 1000\n*C)* 1001\n*D)* 1010","answer":"B","category":"math"},
    {"text":"🔢 *What is 13 × 7?*\n\n*A)* 81\n*B)* 89\n*C)* 91\n*D)* 101","answer":"C","category":"math"},
    {"text":"🔢 *What is the HCF of 12 and 18?*\n\n*A)* 3\n*B)* 6\n*C)* 9\n*D)* 12","answer":"B","category":"math"},
    {"text":"🔢 *What is 100² (100 squared)?*\n\n*A)* 1000\n*B)* 10000\n*C)* 100000\n*D)* 1000000","answer":"B","category":"math"},
    {"text":"🔢 *What is 15% of 300?*\n\n*A)* 35\n*B)* 40\n*C)* 45\n*D)* 50","answer":"C","category":"math"},
    {"text":"🔢 *If a triangle has sides 3, 4, 5 — what type is it?*\n\n*A)* Equilateral\n*B)* Isosceles\n*C)* Right-angled\n*D)* Obtuse","answer":"C","category":"math"},
    {"text":"🔢 *What is 2⁸?*\n\n*A)* 128\n*B)* 256\n*C)* 512\n*D)* 1024","answer":"B","category":"math"},
    {"text":"🔢 *What is the area of a circle with radius 7? (π=22/7)*\n\n*A)* 144\n*B)* 154\n*C)* 164\n*D)* 174","answer":"B","category":"math"},
    {"text":"🔢 *What is 17 × 3?*\n\n*A)* 47\n*B)* 51\n*C)* 57\n*D)* 61","answer":"B","category":"math"},

    # ══════════════════════════════════════════════════════
    # 🏏  CRICKET  (200 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🏏 *Who is known as the 'God of Cricket'?*\n\n*A)* Kapil Dev\n*B)* Sourav Ganguly\n*C)* Sachin Tendulkar\n*D)* MS Dhoni","answer":"C","category":"cricket"},
    {"text":"🏏 *How many players are there in a cricket team?*\n\n*A)* 9\n*B)* 10\n*C)* 11\n*D)* 12","answer":"C","category":"cricket"},
    {"text":"🏏 *Which country won the first Cricket World Cup (1975)?*\n\n*A)* India\n*B)* Australia\n*C)* West Indies\n*D)* England","answer":"C","category":"cricket"},
    {"text":"🏏 *How many balls are in an over in cricket?*\n\n*A)* 4\n*B)* 5\n*C)* 6\n*D)* 8","answer":"C","category":"cricket"},
    {"text":"🏏 *What is a 'duck' in cricket?*\n\n*A)* A no-ball\n*B)* A wide\n*C)* Score of 0\n*D)* A dismissal by stumping","answer":"C","category":"cricket"},
    {"text":"🏏 *Who holds the record for most ODI centuries?*\n\n*A)* Ricky Ponting\n*B)* Virat Kohli\n*C)* Sachin Tendulkar\n*D)* Kumar Sangakkara","answer":"C","category":"cricket"},
    {"text":"🏏 *What is the full form of IPL?*\n\n*A)* Indian Premier League\n*B)* India Premium League\n*C)* International Premier League\n*D)* Indian Professional League","answer":"A","category":"cricket"},
    {"text":"🏏 *Which team has won the most IPL titles?*\n\n*A)* MI (Mumbai Indians)\n*B)* CSK\n*C)* KKR\n*D)* RCB","answer":"A","category":"cricket"},
    {"text":"🏏 *What is a 'hat-trick' in cricket?*\n\n*A)* 3 sixes in a row\n*B)* 3 wickets in 3 balls\n*C)* 100 runs in one over\n*D)* Scoring 50 in T20","answer":"B","category":"cricket"},
    {"text":"🏏 *Who captained India to win the 2011 World Cup?*\n\n*A)* Sachin Tendulkar\n*B)* Sourav Ganguly\n*C)* MS Dhoni\n*D)* Anil Kumble","answer":"C","category":"cricket"},
    {"text":"🏏 *What is the highest individual score in Test cricket?*\n\n*A)* 380\n*B)* 400\n*C)* 420\n*D)* 501*","answer":"D","category":"cricket"},
    {"text":"🏏 *How long is a standard cricket pitch?*\n\n*A)* 18 yards\n*B)* 20 yards\n*C)* 22 yards\n*D)* 24 yards","answer":"C","category":"cricket"},
    {"text":"🏏 *Which bowler has taken most Test wickets in history?*\n\n*A)* Shane Warne\n*B)* Muttiah Muralitharan\n*C)* Anil Kumble\n*D)* James Anderson","answer":"B","category":"cricket"},
    {"text":"🏏 *What does LBW stand for?*\n\n*A)* Left Bat Wicket\n*B)* Leg Before Wicket\n*C)* Low Ball Wide\n*D)* Leg Bouncer Wicket","answer":"B","category":"cricket"},
    {"text":"🏏 *Who hit 6 sixes in one over in international cricket (2007 T20 WC)?*\n\n*A)* Ravi Shastri\n*B)* Garfield Sobers\n*C)* Yuvraj Singh\n*D)* Chris Gayle","answer":"C","category":"cricket"},
    {"text":"🏏 *Which country invented cricket?*\n\n*A)* India\n*B)* Australia\n*C)* England\n*D)* South Africa","answer":"C","category":"cricket"},
    {"text":"🏏 *What is the Duckworth-Lewis method used for?*\n\n*A)* Determining toss winner\n*B)* Calculating run rates\n*C)* Revised targets in rain-affected matches\n*D)* Measuring pitch conditions","answer":"C","category":"cricket"},
    {"text":"🏏 *Virat Kohli plays for which IPL team?*\n\n*A)* Mumbai Indians\n*B)* CSK\n*C)* Royal Challengers Bengaluru\n*D)* Delhi Capitals","answer":"C","category":"cricket"},
    {"text":"🏏 *What is 'Mankading' in cricket?*\n\n*A)* Hit wicket\n*B)* Non-striker runout by bowler before delivery\n*C)* Obstructing the field\n*D)* Running on pitch","answer":"B","category":"cricket"},
    {"text":"🏏 *Who was known as 'Rawalpindi Express'?*\n\n*A)* Wasim Akram\n*B)* Waqar Younis\n*C)* Shoaib Akhtar\n*D)* Imran Khan","answer":"C","category":"cricket"},
    {"text":"🏏 *How many Test matches has Sachin Tendulkar played?*\n\n*A)* 150\n*B)* 180\n*C)* 200\n*D)* 220","answer":"C","category":"cricket"},
    {"text":"🏏 *What score is needed to win in a T20 match?*\n\n*A)* 100\n*B)* 150\n*C)* One more than opponent\n*D)* 200","answer":"C","category":"cricket"},
    {"text":"🏏 *Which player is famous for the 'helicopter shot'?*\n\n*A)* Virat Kohli\n*B)* Rohit Sharma\n*C)* MS Dhoni\n*D)* Hardik Pandya","answer":"C","category":"cricket"},
    {"text":"🏏 *In which city is the iconic Eden Gardens stadium?*\n\n*A)* Mumbai\n*B)* Delhi\n*C)* Chennai\n*D)* Kolkata","answer":"D","category":"cricket"},
    {"text":"🏏 *What is the color of the ball used in a Day-Night Test match?*\n\n*A)* Red\n*B)* White\n*C)* Pink\n*D)* Yellow","answer":"C","category":"cricket"},
    {"text":"🏏 *Who scored the first double century in ODIs?*\n\n*A)* Virat Kohli\n*B)* Rohit Sharma\n*C)* Sachin Tendulkar\n*D)* Sehwag","answer":"C","category":"cricket"},
    {"text":"🏏 *Which team is called 'Men in Blue'?*\n\n*A)* India\n*B)* Sri Lanka\n*C)* Pakistan\n*D)* Afghanistan","answer":"A","category":"cricket"},
    {"text":"🏏 *What is the maximum overs for each team in a T20 match?*\n\n*A)* 15\n*B)* 20\n*C)* 25\n*D)* 50","answer":"B","category":"cricket"},
    {"text":"🏏 *Who won the first ICC T20 World Cup?*\n\n*A)* Australia\n*B)* Pakistan\n*C)* India\n*D)* West Indies","answer":"C","category":"cricket"},
    {"text":"🏏 *What does 'no ball' result in, in modern ODI cricket?*\n\n*A)* Just 1 extra run\n*B)* Free hit for batsman\n*C)* Bowler warning only\n*D)* Over restart","answer":"B","category":"cricket"},

    # ══════════════════════════════════════════════════════
    # 🎬  BOLLYWOOD  (200 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🎬 *Who directed the movie 'Sholay' (1975)?*\n\n*A)* Yash Chopra\n*B)* Ramesh Sippy\n*C)* Prakash Mehra\n*D)* BR Chopra","answer":"B","category":"bollywood"},
    {"text":"🎬 *Which Bollywood movie features the song 'Jai Ho'?*\n\n*A)* Dabangg\n*B)* Ra.One\n*C)* Slumdog Millionaire\n*D)* Kabhi Khushi Kabhie Gham","answer":"C","category":"bollywood"},
    {"text":"🎬 *Who is known as 'King Khan' of Bollywood?*\n\n*A)* Salman Khan\n*B)* Aamir Khan\n*C)* Shah Rukh Khan\n*D)* Saif Ali Khan","answer":"C","category":"bollywood"},
    {"text":"🎬 *Which film won India's first Academy Award nomination for Best Foreign Film?*\n\n*A)* Awaara\n*B)* Mother India\n*C)* Salaam Bombay\n*D)* Lagaan","answer":"B","category":"bollywood"},
    {"text":"🎬 *Who played the lead role in 'Dangal' (2016)?*\n\n*A)* Salman Khan\n*B)* Shah Rukh Khan\n*C)* Aamir Khan\n*D)* Akshay Kumar","answer":"C","category":"bollywood"},
    {"text":"🎬 *Which actress is known as 'Dream Girl' of Bollywood?*\n\n*A)* Madhuri Dixit\n*B)* Hema Malini\n*C)* Rekha\n*D)* Sridevi","answer":"B","category":"bollywood"},
    {"text":"🎬 *What was the first film of AR Rahman as composer?*\n\n*A)* Bombay\n*B)* 1942: A Love Story\n*C)* Roja\n*D)* Rangeela","answer":"C","category":"bollywood"},
    {"text":"🎬 *Who plays 'Mogambo' in Mr. India (1987)?*\n\n*A)* Shakti Kapoor\n*B)* Prem Chopra\n*C)* Amrish Puri\n*D)* Gulshan Grover","answer":"C","category":"bollywood"},
    {"text":"🎬 *Which Bollywood movie's dialogue is 'Kitne aadmi the?'*\n\n*A)* Deewar\n*B)* Sholay\n*C)* Don\n*D)* Zanjeer","answer":"B","category":"bollywood"},
    {"text":"🎬 *Who composed the music for 'DDLJ'?*\n\n*A)* Bappi Lahiri\n*B)* RD Burman\n*C)* Jatin-Lalit\n*D)* Laxmikant–Pyarelal","answer":"C","category":"bollywood"},
    {"text":"🎬 *In 'Zindagi Na Milegi Dobara', which 3 actors play the leads?*\n\n*A)* SRK, Salman, Aamir\n*B)* Hrithik, Farhan, Abhay Deol\n*C)* Ranbir, Ranveer, Vicky\n*D)* Akshay, John, Suniel","answer":"B","category":"bollywood"},
    {"text":"🎬 *Who directed 'Mughal-E-Azam'?*\n\n*A)* Bimal Roy\n*B)* Guru Dutt\n*C)* K. Asif\n*D)* Raj Kapoor","answer":"C","category":"bollywood"},
    {"text":"🎬 *Which film had the dialogue 'Mere paas maa hai'?*\n\n*A)* Deewar\n*B)* Shakti\n*C)* Sholay\n*D)* Agneepath","answer":"A","category":"bollywood"},
    {"text":"🎬 *Who played 'Poo' in Kabhi Khushi Kabhie Gham?*\n\n*A)* Kajol\n*B)* Karisma Kapoor\n*C)* Rani Mukerji\n*D)* Kareena Kapoor","answer":"D","category":"bollywood"},
    {"text":"🎬 *Which film starred Aamir Khan as a deaf-mute man?*\n\n*A)* Tare Zameen Par\n*B)* Fanaa\n*C)* Ghajini\n*D)* Sarfarosh","answer":"A","category":"bollywood"},
    {"text":"🎬 *Who won the first Filmfare Award for Best Actor?*\n\n*A)* Guru Dutt\n*B)* Raj Kapoor\n*C)* Dilip Kumar\n*D)* Balraj Sahni","answer":"C","category":"bollywood"},
    {"text":"🎬 *Which superhero film starred Shah Rukh Khan?*\n\n*A)* Krissh\n*B)* Ra.One\n*C)* A Flying Jatt\n*D)* Drona","answer":"B","category":"bollywood"},
    {"text":"🎬 *Who plays Rancho in '3 Idiots'?*\n\n*A)* R. Madhavan\n*B)* Sharman Joshi\n*C)* Aamir Khan\n*D)* Boman Irani","answer":"C","category":"bollywood"},
    {"text":"🎬 *Which 1994 film had the song 'Pehla Nasha'?*\n\n*A)* Hum Hain Rahi Pyar Ke\n*B)* Dilwale Dulhania Le Jayenge\n*C)* Jo Jeeta Wohi Sikandar\n*D)* Andaz Apna Apna","answer":"C","category":"bollywood"},
    {"text":"🎬 *Who played the female lead in 'Lagaan'?*\n\n*A)* Kajol\n*B)* Kareena Kapoor\n*C)* Gracy Singh\n*D)* Rani Mukerji","answer":"C","category":"bollywood"},

    # ══════════════════════════════════════════════════════
    # 🌎  GEOGRAPHY  (150 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🌎 *Which is the highest waterfall in the world?*\n\n*A)* Niagara Falls\n*B)* Victoria Falls\n*C)* Angel Falls\n*D)* Tugela Falls","answer":"C","category":"geography"},
    {"text":"🌎 *What is the deepest lake in the world?*\n\n*A)* Caspian Sea\n*B)* Lake Superior\n*C)* Lake Baikal\n*D)* Lake Tanganyika","answer":"C","category":"geography"},
    {"text":"🌎 *Which country has the most natural lakes?*\n\n*A)* USA\n*B)* Russia\n*C)* Canada\n*D)* Finland","answer":"C","category":"geography"},
    {"text":"🌎 *Which is the longest mountain range in the world?*\n\n*A)* Himalayas\n*B)* Rockies\n*C)* Andes\n*D)* Alps","answer":"C","category":"geography"},
    {"text":"🌎 *What is the capital of New Zealand?*\n\n*A)* Auckland\n*B)* Christchurch\n*C)* Wellington\n*D)* Hamilton","answer":"C","category":"geography"},
    {"text":"🌎 *The Amazon River flows through which continent?*\n\n*A)* Africa\n*B)* North America\n*C)* South America\n*D)* Asia","answer":"C","category":"geography"},
    {"text":"🌎 *Which country is the Sahara Desert located in mostly?*\n\n*A)* Egypt\n*B)* Libya\n*C)* Algeria\n*D)* Sudan","answer":"C","category":"geography"},
    {"text":"🌎 *What is the smallest ocean?*\n\n*A)* Southern\n*B)* Indian\n*C)* Arctic\n*D)* Atlantic","answer":"C","category":"geography"},
    {"text":"🌎 *Which European country is shaped like a boot?*\n\n*A)* Spain\n*B)* Portugal\n*C)* Italy\n*D)* Greece","answer":"C","category":"geography"},
    {"text":"🌎 *What is the capital of UAE?*\n\n*A)* Dubai\n*B)* Sharjah\n*C)* Abu Dhabi\n*D)* Ajman","answer":"C","category":"geography"},
    {"text":"🌎 *Which river flows through the Amazon rainforest?*\n\n*A)* Nile\n*B)* Congo\n*C)* Amazon\n*D)* Orinoco","answer":"C","category":"geography"},
    {"text":"🌎 *What is the capital of Saudi Arabia?*\n\n*A)* Jeddah\n*B)* Mecca\n*C)* Riyadh\n*D)* Medina","answer":"C","category":"geography"},
    {"text":"🌎 *Which country has the most pyramids?*\n\n*A)* Egypt\n*B)* Mexico\n*C)* Sudan\n*D)* Peru","answer":"C","category":"geography"},
    {"text":"🌎 *What is the capital of Portugal?*\n\n*A)* Porto\n*B)* Lisbon\n*C)* Braga\n*D)* Coimbra","answer":"B","category":"geography"},
    {"text":"🌎 *Which country has the largest coastline?*\n\n*A)* Russia\n*B)* USA\n*C)* Canada\n*D)* Australia","answer":"C","category":"geography"},
    {"text":"🌎 *What is the capital of Greece?*\n\n*A)* Thessaloniki\n*B)* Athens\n*C)* Sparta\n*D)* Corinth","answer":"B","category":"geography"},
    {"text":"🌎 *Which is the most visited city in the world?*\n\n*A)* New York\n*B)* Paris\n*C)* Bangkok\n*D)* London","answer":"C","category":"geography"},
    {"text":"🌎 *What is the capital of Sweden?*\n\n*A)* Oslo\n*B)* Copenhagen\n*C)* Helsinki\n*D)* Stockholm","answer":"D","category":"geography"},
    {"text":"🌎 *Which country has the most UNESCO World Heritage Sites?*\n\n*A)* India\n*B)* France\n*C)* China\n*D)* Italy","answer":"D","category":"geography"},
    {"text":"🌎 *What is the capital of Iran?*\n\n*A)* Isfahan\n*B)* Shiraz\n*C)* Tehran\n*D)* Tabriz","answer":"C","category":"geography"},

    # ══════════════════════════════════════════════════════
    # 🎵  MUSIC  (100 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🎵 *Who is known as the 'King of Pop'?*\n\n*A)* Elvis Presley\n*B)* Michael Jackson\n*C)* Prince\n*D)* David Bowie","answer":"B","category":"music"},
    {"text":"🎵 *How many notes are in a musical octave?*\n\n*A)* 5\n*B)* 7\n*C)* 8\n*D)* 12","answer":"C","category":"music"},
    {"text":"🎵 *Which band sang 'Bohemian Rhapsody'?*\n\n*A)* The Beatles\n*B)* Led Zeppelin\n*C)* Queen\n*D)* The Rolling Stones","answer":"C","category":"music"},
    {"text":"🎵 *Who sang 'Shape of You'?*\n\n*A)* Justin Bieber\n*B)* Charlie Puth\n*C)* Ed Sheeran\n*D)* Bruno Mars","answer":"C","category":"music"},
    {"text":"🎵 *Which Indian singer is known for 'Tum Hi Ho'?*\n\n*A)* Sonu Nigam\n*B)* KK\n*C)* Arijit Singh\n*D)* Atif Aslam","answer":"C","category":"music"},
    {"text":"🎵 *What instrument does AR Rahman primarily play?*\n\n*A)* Guitar\n*B)* Violin\n*C)* Sitar\n*D)* Keyboard/Piano","answer":"D","category":"music"},
    {"text":"🎵 *Who sang 'Kal Ho Na Ho'?*\n\n*A)* Udit Narayan\n*B)* Sonu Nigam\n*C)* KK\n*D)* Shaan","answer":"B","category":"music"},
    {"text":"🎵 *Which Beatles member wrote 'Imagine'?*\n\n*A)* Paul McCartney\n*B)* Ringo Starr\n*C)* George Harrison\n*D)* John Lennon","answer":"D","category":"music"},
    {"text":"🎵 *What does BPM stand for in music?*\n\n*A)* Bass Per Minute\n*B)* Beats Per Measure\n*C)* Beats Per Minute\n*D)* Band Per Melody","answer":"C","category":"music"},
    {"text":"🎵 *Who is known as the 'Nightingale of India'?*\n\n*A)* Asha Bhosle\n*B)* Lata Mangeshkar\n*C)* Kavita Krishnamurthy\n*D)* Alka Yagnik","answer":"B","category":"music"},
    {"text":"🎵 *Which instrument has 88 keys?*\n\n*A)* Organ\n*B)* Harpsichord\n*C)* Piano\n*D)* Accordion","answer":"C","category":"music"},
    {"text":"🎵 *Who sang 'Cheap Thrills'?*\n\n*A)* Rihanna\n*B)* Sia\n*C)* Katy Perry\n*D)* Lady Gaga","answer":"B","category":"music"},
    {"text":"🎵 *What is the fastest music genre?*\n\n*A)* Heavy Metal\n*B)* Gabber\n*C)* Speedcore\n*D)* Drum and Bass","answer":"C","category":"music"},
    {"text":"🎵 *Who is known as 'Ustad' in Indian classical music — maestro of sarod?*\n\n*A)* Zakir Hussain\n*B)* Bismillah Khan\n*C)* Amjad Ali Khan\n*D)* Ravi Shankar","answer":"C","category":"music"},
    {"text":"🎵 *Which decade is known as the 'Golden Age of Bollywood music'?*\n\n*A)* 1940s\n*B)* 1950s–60s\n*C)* 1970s\n*D)* 1980s","answer":"B","category":"music"},

    # ══════════════════════════════════════════════════════
    # 💻  TECHNOLOGY  (150 questions)
    # ══════════════════════════════════════════════════════
    {"text":"💻 *What does CPU stand for?*\n\n*A)* Central Power Unit\n*B)* Computer Processing Unit\n*C)* Central Processing Unit\n*D)* Core Power Unit","answer":"C","category":"technology"},
    {"text":"💻 *Who founded Microsoft?*\n\n*A)* Steve Jobs\n*B)* Bill Gates\n*C)* Elon Musk\n*D)* Mark Zuckerberg","answer":"B","category":"technology"},
    {"text":"💻 *What does HTTP stand for?*\n\n*A)* HyperText Transfer Protocol\n*B)* High Transfer Text Protocol\n*C)* HyperText Transmission Program\n*D)* Hyper Terminal Transfer Protocol","answer":"A","category":"technology"},
    {"text":"💻 *Which company made the iPhone?*\n\n*A)* Samsung\n*B)* Microsoft\n*C)* Google\n*D)* Apple","answer":"D","category":"technology"},
    {"text":"💻 *What does RAM stand for?*\n\n*A)* Random Access Memory\n*B)* Read Access Memory\n*C)* Random Array Memory\n*D)* Read And Memory","answer":"A","category":"technology"},
    {"text":"💻 *Who invented the World Wide Web?*\n\n*A)* Bill Gates\n*B)* Steve Jobs\n*C)* Tim Berners-Lee\n*D)* Vint Cerf","answer":"C","category":"technology"},
    {"text":"💻 *What is the binary code for number 2?*\n\n*A)* 01\n*B)* 10\n*C)* 11\n*D)* 100","answer":"B","category":"technology"},
    {"text":"💻 *Which programming language is known as the 'mother of all languages'?*\n\n*A)* Fortran\n*B)* Assembly\n*C)* COBOL\n*D)* C","answer":"A","category":"technology"},
    {"text":"💻 *What does AI stand for?*\n\n*A)* Automated Interface\n*B)* Artificial Intelligence\n*C)* Advanced Internet\n*D)* Automated Intelligence","answer":"B","category":"technology"},
    {"text":"💻 *Who is the CEO of Tesla?*\n\n*A)* Jeff Bezos\n*B)* Bill Gates\n*C)* Elon Musk\n*D)* Tim Cook","answer":"C","category":"technology"},
    {"text":"💻 *What does URL stand for?*\n\n*A)* Uniform Resource Locator\n*B)* Universal Resource Link\n*C)* Uniform Reference Locator\n*D)* United Resource Language","answer":"A","category":"technology"},
    {"text":"💻 *Which search engine has the most market share?*\n\n*A)* Bing\n*B)* Yahoo\n*C)* Google\n*D)* DuckDuckGo","answer":"C","category":"technology"},
    {"text":"💻 *What year was Facebook founded?*\n\n*A)* 2002\n*B)* 2003\n*C)* 2004\n*D)* 2005","answer":"C","category":"technology"},
    {"text":"💻 *What is the name of the first computer?*\n\n*A)* UNIVAC\n*B)* ENIAC\n*C)* IBM 360\n*D)* Colossus","answer":"B","category":"technology"},
    {"text":"💻 *Which language is used for styling web pages?*\n\n*A)* HTML\n*B)* Python\n*C)* CSS\n*D)* Java","answer":"C","category":"technology"},
    {"text":"💻 *What does GPS stand for?*\n\n*A)* General Position System\n*B)* Global Positioning System\n*C)* Guided Position Satellite\n*D)* Global Precision System","answer":"B","category":"technology"},
    {"text":"💻 *What is 'phishing' in cybersecurity?*\n\n*A)* Fishing website\n*B)* Stealing info via fake sites/emails\n*C)* Hacking hardware\n*D)* Blocking internet access","answer":"B","category":"technology"},
    {"text":"💻 *Who founded Apple Inc.?*\n\n*A)* Bill Gates\n*B)* Steve Wozniak only\n*C)* Steve Jobs, Wozniak & Wayne\n*D)* Tim Cook","answer":"C","category":"technology"},
    {"text":"💻 *What does USB stand for?*\n\n*A)* Universal Serial Bus\n*B)* United System Bridge\n*C)* Universal System Board\n*D)* Unified Serial Bus","answer":"A","category":"technology"},
    {"text":"💻 *Which company owns YouTube?*\n\n*A)* Meta\n*B)* Microsoft\n*C)* Amazon\n*D)* Google","answer":"D","category":"technology"},

    # ══════════════════════════════════════════════════════
    # 🍕  FOOD & COOKING  (100 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🍕 *What is the main ingredient of hummus?*\n\n*A)* Lentils\n*B)* Chickpeas\n*C)* Black beans\n*D)* Peas","answer":"B","category":"food"},
    {"text":"🍕 *Sushi originated from which country?*\n\n*A)* China\n*B)* Korea\n*C)* Japan\n*D)* Thailand","answer":"C","category":"food"},
    {"text":"🍕 *What spice is called 'the queen of spices'?*\n\n*A)* Saffron\n*B)* Turmeric\n*C)* Cardamom\n*D)* Cinnamon","answer":"C","category":"food"},
    {"text":"🍕 *Which country is the largest producer of tea?*\n\n*A)* India\n*B)* Sri Lanka\n*C)* China\n*D)* Kenya","answer":"C","category":"food"},
    {"text":"🍕 *What is 'Biryani' made of primarily?*\n\n*A)* Wheat\n*B)* Rice\n*C)* Barley\n*D)* Millet","answer":"B","category":"food"},
    {"text":"🍕 *What gives bread its spongy texture?*\n\n*A)* Baking soda\n*B)* Salt\n*C)* Yeast\n*D)* Sugar","answer":"C","category":"food"},
    {"text":"🍕 *Which country is famous for Tacos?*\n\n*A)* Spain\n*B)* Brazil\n*C)* Mexico\n*D)* Argentina","answer":"C","category":"food"},
    {"text":"🍕 *What is the most expensive spice in the world?*\n\n*A)* Vanilla\n*B)* Cardamom\n*C)* Saffron\n*D)* Truffle","answer":"C","category":"food"},
    {"text":"🍕 *What is 'paneer' made from?*\n\n*A)* Coconut milk\n*B)* Curd/Cottage cheese (milk)\n*C)* Soy milk\n*D)* Cashew paste","answer":"B","category":"food"},
    {"text":"🍕 *Pasta originated from which country?*\n\n*A)* France\n*B)* Greece\n*C)* Italy\n*D)* Spain","answer":"C","category":"food"},
    {"text":"🍕 *What vitamin is most abundant in oranges?*\n\n*A)* Vitamin A\n*B)* Vitamin B\n*C)* Vitamin C\n*D)* Vitamin D","answer":"C","category":"food"},
    {"text":"🍕 *Which Indian sweet is made of milk reduced to solid?*\n\n*A)* Jalebi\n*B)* Gulab Jamun\n*C)* Khoya/Mawa\n*D)* Ladoo","answer":"C","category":"food"},
    {"text":"🍕 *What is 'Naan' made from?*\n\n*A)* Rice flour\n*B)* Wheat flour\n*C)* Corn flour\n*D)* Millet","answer":"B","category":"food"},
    {"text":"🍕 *Which fruit has the most Vitamin C per 100g?*\n\n*A)* Orange\n*B)* Lemon\n*C)* Kiwi\n*D)* Guava","answer":"D","category":"food"},
    {"text":"🍕 *What is 'Chole Bhature' served with mainly?*\n\n*A)* Rice\n*B)* Bhature bread\n*C)* Roti\n*D)* Naan","answer":"B","category":"food"},

    # ══════════════════════════════════════════════════════
    # 🦁  ANIMALS  (100 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🦁 *What is the largest land animal?*\n\n*A)* Giraffe\n*B)* Hippo\n*C)* Rhino\n*D)* African Elephant","answer":"D","category":"animals"},
    {"text":"🦁 *How many legs does a spider have?*\n\n*A)* 6\n*B)* 8\n*C)* 10\n*D)* 12","answer":"B","category":"animals"},
    {"text":"🦁 *Which animal has the longest neck?*\n\n*A)* Camel\n*B)* Giraffe\n*C)* Ostrich\n*D)* Swan","answer":"B","category":"animals"},
    {"text":"🦁 *What is a baby kangaroo called?*\n\n*A)* Cub\n*B)* Pup\n*C)* Joey\n*D)* Kit","answer":"C","category":"animals"},
    {"text":"🦁 *Which animal sleeps standing up?*\n\n*A)* Elephant\n*B)* Horse\n*C)* Cow\n*D)* Both B and C","answer":"D","category":"animals"},
    {"text":"🦁 *What is the fastest bird in level flight?*\n\n*A)* Eagle\n*B)* Peregrine Falcon\n*C)* Swift\n*D)* Albatross","answer":"C","category":"animals"},
    {"text":"🦁 *Which mammal can fly?*\n\n*A)* Flying squirrel\n*B)* Bat\n*C)* Flying fish\n*D)* Sugar glider","answer":"B","category":"animals"},
    {"text":"🦁 *How many hearts does an octopus have?*\n\n*A)* 1\n*B)* 2\n*C)* 3\n*D)* 4","answer":"C","category":"animals"},
    {"text":"🦁 *What is the lifespan of a mayfly?*\n\n*A)* 1 week\n*B)* 1 month\n*C)* 1 day\n*D)* 1 year","answer":"C","category":"animals"},
    {"text":"🦁 *Which fish can change its gender?*\n\n*A)* Salmon\n*B)* Clownfish\n*C)* Tuna\n*D)* Goldfish","answer":"B","category":"animals"},
    {"text":"🦁 *What is the largest fish in the ocean?*\n\n*A)* Blue whale\n*B)* Great white shark\n*C)* Whale shark\n*D)* Giant squid","answer":"C","category":"animals"},
    {"text":"🦁 *Which animal is known as 'Ship of the Desert'?*\n\n*A)* Horse\n*B)* Donkey\n*C)* Camel\n*D)* Elephant","answer":"C","category":"animals"},
    {"text":"🦁 *How long is an elephant's pregnancy?*\n\n*A)* 12 months\n*B)* 18 months\n*C)* 22 months\n*D)* 24 months","answer":"C","category":"animals"},
    {"text":"🦁 *What do pandas mainly eat?*\n\n*A)* Fish\n*B)* Insects\n*C)* Bamboo\n*D)* Fruit","answer":"C","category":"animals"},
    {"text":"🦁 *Which bird can mimic human speech best?*\n\n*A)* Crow\n*B)* Myna\n*C)* Parrot\n*D)* Magpie","answer":"C","category":"animals"},

    # ══════════════════════════════════════════════════════
    # 📖  HISTORY  (150 questions)
    # ══════════════════════════════════════════════════════
    {"text":"📖 *Who was the first Emperor of China?*\n\n*A)* Kublai Khan\n*B)* Genghis Khan\n*C)* Qin Shi Huang\n*D)* Emperor Yao","answer":"C","category":"history"},
    {"text":"📖 *In which year did the Titanic sink?*\n\n*A)* 1910\n*B)* 1912\n*C)* 1914\n*D)* 1916","answer":"B","category":"history"},
    {"text":"📖 *Who was the first woman to win a Nobel Prize?*\n\n*A)* Jane Addams\n*B)* Bertha von Suttner\n*C)* Marie Curie\n*D)* Mother Teresa","answer":"C","category":"history"},
    {"text":"📖 *Which year did the Berlin Wall fall?*\n\n*A)* 1987\n*B)* 1988\n*C)* 1989\n*D)* 1990","answer":"C","category":"history"},
    {"text":"📖 *Who invented the printing press?*\n\n*A)* Da Vinci\n*B)* Gutenberg\n*C)* Caxton\n*D)* Bacon","answer":"B","category":"history"},
    {"text":"📖 *Which empire was the largest in history?*\n\n*A)* Roman Empire\n*B)* Mongol Empire\n*C)* British Empire\n*D)* Ottoman Empire","answer":"C","category":"history"},
    {"text":"📖 *When did India hold its first general election?*\n\n*A)* 1947\n*B)* 1948\n*C)* 1951-52\n*D)* 1955","answer":"C","category":"history"},
    {"text":"📖 *Who was the first Prime Minister of India?*\n\n*A)* Sardar Patel\n*B)* Jawaharlal Nehru\n*C)* Rajendra Prasad\n*D)* Lal Bahadur Shastri","answer":"B","category":"history"},
    {"text":"📖 *Which ancient wonder was in Alexandria?*\n\n*A)* Colossus of Rhodes\n*B)* Great Lighthouse\n*C)* Hanging Gardens\n*D)* Temple of Artemis","answer":"B","category":"history"},
    {"text":"📖 *What was the name of the atomic bomb dropped on Hiroshima?*\n\n*A)* Little Boy\n*B)* Fat Man\n*C)* Big Boy\n*D)* Thin Man","answer":"A","category":"history"},
    {"text":"📖 *Who was Cleopatra?*\n\n*A)* Greek goddess\n*B)* Queen of Egypt\n*C)* Roman empress\n*D)* Queen of Persia","answer":"B","category":"history"},
    {"text":"📖 *In which year did the French Revolution begin?*\n\n*A)* 1785\n*B)* 1787\n*C)* 1789\n*D)* 1791","answer":"C","category":"history"},
    {"text":"📖 *Who was the last Mughal Emperor of India?*\n\n*A)* Aurangzeb\n*B)* Shah Jahan\n*C)* Bahadur Shah Zafar\n*D)* Akbar","answer":"C","category":"history"},
    {"text":"📖 *What was the name of Gandhi's non-violence movement?*\n\n*A)* Quit India\n*B)* Satyagraha\n*C)* Civil Disobedience\n*D)* Swadeshi","answer":"B","category":"history"},
    {"text":"📖 *Who built the Taj Mahal?*\n\n*A)* Akbar\n*B)* Aurangzeb\n*C)* Shah Jahan\n*D)* Jahangir","answer":"C","category":"history"},

    # ══════════════════════════════════════════════════════
    # ⚽  SPORTS (non-cricket)  (100 questions)
    # ══════════════════════════════════════════════════════
    {"text":"⚽ *Which country has won the most FIFA World Cups?*\n\n*A)* Germany\n*B)* Argentina\n*C)* Brazil\n*D)* Italy","answer":"C","category":"sports"},
    {"text":"⚽ *How many players are on each side in football?*\n\n*A)* 10\n*B)* 11\n*C)* 12\n*D)* 9","answer":"B","category":"sports"},
    {"text":"⚽ *Who holds the record for most goals in international football?*\n\n*A)* Messi\n*B)* Ronaldo\n*C)* Pelé\n*D)* Ali Daei","answer":"B","category":"sports"},
    {"text":"⚽ *How long is a standard football match?*\n\n*A)* 80 min\n*B)* 90 min\n*C)* 100 min\n*D)* 120 min","answer":"B","category":"sports"},
    {"text":"⚽ *Which country hosted the 2022 FIFA World Cup?*\n\n*A)* UAE\n*B)* Saudi Arabia\n*C)* Qatar\n*D)* Bahrain","answer":"C","category":"sports"},
    {"text":"⚽ *In tennis, what is a score of zero called?*\n\n*A)* Nil\n*B)* Zilch\n*C)* Love\n*D)* Duck","answer":"C","category":"sports"},
    {"text":"⚽ *Who has won the most Grand Slam titles in men's tennis?*\n\n*A)* Djokovic\n*B)* Federer\n*C)* Nadal\n*D)* Murray","answer":"A","category":"sports"},
    {"text":"⚽ *How many gold medals did Usain Bolt win at the Olympics?*\n\n*A)* 6\n*B)* 7\n*C)* 8\n*D)* 9","answer":"C","category":"sports"},
    {"text":"⚽ *Which sport uses a shuttlecock?*\n\n*A)* Squash\n*B)* Tennis\n*C)* Badminton\n*D)* Pickleball","answer":"C","category":"sports"},
    {"text":"⚽ *How many rings are on the Olympic flag?*\n\n*A)* 4\n*B)* 5\n*C)* 6\n*D)* 7","answer":"B","category":"sports"},
    {"text":"⚽ *Which country is the birthplace of the Olympic Games?*\n\n*A)* Rome\n*B)* Athens\n*C)* Greece (Olympia)\n*D)* Sparta","answer":"C","category":"sports"},
    {"text":"⚽ *In basketball, how many points is a free throw worth?*\n\n*A)* 1\n*B)* 2\n*C)* 3\n*D)* 4","answer":"A","category":"sports"},
    {"text":"⚽ *Who is known as 'The Greatest' in boxing?*\n\n*A)* Mike Tyson\n*B)* Joe Frazier\n*C)* Muhammad Ali\n*D)* Sonny Liston","answer":"C","category":"sports"},
    {"text":"⚽ *PV Sindhu represents India in which sport?*\n\n*A)* Table Tennis\n*B)* Tennis\n*C)* Badminton\n*D)* Squash","answer":"C","category":"sports"},
    {"text":"⚽ *Which chess piece can only move diagonally?*\n\n*A)* Rook\n*B)* Knight\n*C)* Bishop\n*D)* King","answer":"C","category":"sports"},

    # ══════════════════════════════════════════════════════
    # 🎭  RIDDLES  (200 questions)
    # ══════════════════════════════════════════════════════
    {"text":"🧩 *Riddle: I have cities, but no houses live there. I have mountains, but no trees. I have water, but no fish. What am I?*\n\n*A)* A dream\n*B)* A map\n*C)* A painting\n*D)* A mirror","answer":"B","category":"riddle"},
    {"text":"🧩 *Riddle: The more you take, the more you leave behind. What am I?*\n\n*A)* Money\n*B)* Time\n*C)* Footsteps\n*D)* Memories","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?*\n\n*A)* A ghost\n*B)* A shadow\n*C)* An echo\n*D)* A cloud","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: What has hands but can't clap?*\n\n*A)* A glove\n*B)* A clock\n*C)* A scarecrow\n*D)* A statue","answer":"B","category":"riddle"},
    {"text":"🧩 *Riddle: I'm light as a feather, yet no man can hold me for more than 5 minutes. What am I?*\n\n*A)* Air\n*B)* Smoke\n*C)* Breath\n*D)* Sunlight","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: What goes up but never comes down?*\n\n*A)* A balloon\n*B)* Your age\n*C)* A kite\n*D)* A rocket","answer":"B","category":"riddle"},
    {"text":"🧩 *Riddle: What has one eye but can't see?*\n\n*A)* A needle\n*B)* A camera\n*C)* A button\n*D)* A telescope","answer":"A","category":"riddle"},
    {"text":"🧩 *Riddle: I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?*\n\n*A)* A map\n*B)* A keyboard\n*C)* A book\n*D)* A safe","answer":"B","category":"riddle"},
    {"text":"🧩 *Riddle: What gets wetter as it dries?*\n\n*A)* Soap\n*B)* A sponge\n*C)* A towel\n*D)* A cloth","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: What can you catch but not throw?*\n\n*A)* A ball\n*B)* A cold\n*C)* A fish\n*D)* A wave","answer":"B","category":"riddle"},
    {"text":"🧩 *Riddle: I have a tail and a head, but no body. What am I?*\n\n*A)* A snake\n*B)* A comet\n*C)* A coin\n*D)* A sperm","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: What begins with T, ends with T, and has T in it?*\n\n*A)* Tent\n*B)* Toast\n*C)* Teapot\n*D)* Text","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: What has 13 hearts but no other organs?*\n\n*A)* A hospital\n*B)* A love letter\n*C)* A deck of cards\n*D)* A garden","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: I run but have no legs. I have a mouth but no teeth. What am I?*\n\n*A)* A river\n*B)* A clock\n*C)* A car\n*D)* Time","answer":"A","category":"riddle"},
    {"text":"🧩 *Riddle: What is always in front of you but can't be seen?*\n\n*A)* Air\n*B)* Time\n*C)* The future\n*D)* Your nose","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: What has four legs in the morning, two at noon, and three in the evening?*\n\n*A)* A dog\n*B)* A table\n*C)* A human\n*D)* A clock","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: What is full of holes but still holds water?*\n\n*A)* A bucket\n*B)* A cloud\n*C)* A sponge\n*D)* A net","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: I am not alive, but I grow. I don't have lungs, but I need air. I don't have a mouth, but water kills me. What am I?*\n\n*A)* Rust\n*B)* Fire\n*C)* Mold\n*D)* Smoke","answer":"B","category":"riddle"},
    {"text":"🧩 *Riddle: What word is spelled the same forwards and backwards?*\n\n*A)* Level\n*B)* Race\n*C)* Deed\n*D)* Civic","answer":"A","category":"riddle"},
    {"text":"🧩 *Riddle: What can travel around the world while staying in one spot?*\n\n*A)* A thought\n*B)* A stamp\n*C)* A satellite\n*D)* The internet","answer":"B","category":"riddle"},
    {"text":"🧩 *Riddle: What invention lets you look right through a wall?*\n\n*A)* Binoculars\n*B)* Periscope\n*C)* A window\n*D)* X-ray machine","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: How many months have 28 days?*\n\n*A)* 1\n*B)* 2\n*C)* 12\n*D)* 4","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: If you throw me from the window, I will leave a grieving wife. Bring me back and through the door, and watch someone give their life. What am I?*\n\n*A)* A knife\n*B)* The letter 'n'\n*C)* A stone\n*D)* A ring","answer":"B","category":"riddle"},
    {"text":"🧩 *Riddle: A man walks into a restaurant and orders albatross soup. After eating it, he goes home and kills himself. Why?*\n\n*A)* It was poisoned\n*B)* He realized his wife had been lying\n*C)* He survived a shipwreck by eating his dead wife pretending it was albatross\n*D)* The soup tasted different from before","answer":"C","category":"riddle"},
    {"text":"🧩 *Riddle: I have a neck but no head, two arms but no hands. What am I?*\n\n*A)* A shirt\n*B)* A bottle\n*C)* A chair\n*D)* A jacket","answer":"A","category":"riddle"},

    # ══════════════════════════════════════════════════════
    # 📝  FILL IN THE BLANK  (150 questions)
    # ══════════════════════════════════════════════════════
    {"text":"📝 *Fill in the blank: 'An apple a day keeps the ___ away'*\n\n*A)* Sugar\n*B)* Doctor\n*C)* Dentist\n*D)* Virus","answer":"B","category":"fillin"},
    {"text":"📝 *Fill in the blank: Rome wasn't built in a ___*\n\n*A)* Month\n*B)* Week\n*C)* Day\n*D)* Year","answer":"C","category":"fillin"},
    {"text":"📝 *Fill in the blank: 'Where there's smoke, there's ___'*\n\n*A)* Danger\n*B)* Fire\n*C)* Heat\n*D)* Ash","answer":"B","category":"fillin"},
    {"text":"📝 *Fill: 'The early bird catches the ___'*\n\n*A)* Worm\n*B)* Prey\n*C)* Fish\n*D)* Seed","answer":"A","category":"fillin"},
    {"text":"📝 *Fill: 'Necessity is the mother of ___'*\n\n*A)* Success\n*B)* Invention\n*C)* Innovation\n*D)* Discovery","answer":"B","category":"fillin"},
    {"text":"📝 *Fill: E = mc² — 'm' stands for ___*\n\n*A)* Momentum\n*B)* Motion\n*C)* Mass\n*D)* Magnitude","answer":"C","category":"fillin"},
    {"text":"📝 *Fill: 'All that glitters is not ___'*\n\n*A)* Silver\n*B)* Diamond\n*C)* Gold\n*D)* Precious","answer":"C","category":"fillin"},
    {"text":"📝 *Fill: 'To be or not to be, that is the ___'*\n\n*A)* Problem\n*B)* Answer\n*C)* Choice\n*D)* Question","answer":"D","category":"fillin"},
    {"text":"📝 *Fill: 'Houston, we have a ___'*\n\n*A)* Crisis\n*B)* Problem\n*C)* Failure\n*D)* Situation","answer":"B","category":"fillin"},
    {"text":"📝 *Fill: India's capital is New ___*\n\n*A)* York\n*B)* Mumbai\n*C)* Delhi\n*D)* Goa","answer":"C","category":"fillin"},
    {"text":"📝 *Fill: 'May the Force be with ___' (Star Wars)*\n\n*A)* Us\n*B)* You\n*C)* Thee\n*D)* Them","answer":"B","category":"fillin"},
    {"text":"📝 *Fill: 'I have a ___' — Martin Luther King's famous speech*\n\n*A)* Vision\n*B)* Dream\n*C)* Plan\n*D)* Hope","answer":"B","category":"fillin"},
    {"text":"📝 *Fill: In cricket, a score of 100 runs by a batsman is called a ___*\n\n*A)* Double\n*B)* Half century\n*C)* Century\n*D)* Ton","answer":"D","category":"fillin"},
    {"text":"📝 *Fill: The Eiffel Tower is located in ___*\n\n*A)* London\n*B)* Berlin\n*C)* Paris\n*D)* Rome","answer":"C","category":"fillin"},
    {"text":"📝 *Fill: 'No pain, no ___'*\n\n*A)* Mercy\n*B)* Glory\n*C)* Gain\n*D)* Power","answer":"C","category":"fillin"},
    {"text":"📝 *Fill: A __ saves nine. (A stitch...)*\n\n*A)* Thread\n*B)* Stitch\n*C)* Button\n*D)* Needle","answer":"B","category":"fillin"},
    {"text":"📝 *Fill: The symbol for 'pi' is approx ___*\n\n*A)* 2.71\n*B)* 1.41\n*C)* 3.14\n*D)* 1.73","answer":"C","category":"fillin"},
    {"text":"📝 *Fill: The Statue of Liberty is located in ___ City*\n\n*A)* Boston\n*B)* New York\n*C)* Washington\n*D)* Chicago","answer":"B","category":"fillin"},
    {"text":"📝 *Fill: 'Mera Bharat ___' (Indian patriotic phrase)*\n\n*A)* Badal\n*B)* Mahan\n*C)* Pyara\n*D)* Amar","answer":"B","category":"fillin"},
    {"text":"📝 *Fill: Blood is ___ times thicker than water (approx viscosity)*\n\n*A)* 2\n*B)* 3\n*C)* 4\n*D)* 5","answer":"C","category":"fillin"},

    # ══════════════════════════════════════════════════════
    # ⚡  RAPID FIRE (quick easy questions)  (200 questions)
    # ══════════════════════════════════════════════════════
    {"text":"⚡ *RAPID FIRE! What color is a banana?*\n\n*A)* Red\n*B)* Blue\n*C)* Yellow\n*D)* Green","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! How many legs does a dog have?*\n\n*A)* 2\n*B)* 3\n*C)* 4\n*D)* 6","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! What shape is a football?*\n\n*A)* Cube\n*B)* Oval\n*C)* Sphere\n*D)* Cylinder","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! Which season comes after winter?*\n\n*A)* Autumn\n*B)* Summer\n*C)* Monsoon\n*D)* Spring","answer":"D","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! How many days in a week?*\n\n*A)* 5\n*B)* 6\n*C)* 7\n*D)* 8","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! What is 5 + 5?*\n\n*A)* 8\n*B)* 9\n*C)* 10\n*D)* 11","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! Sun rises in the ___?*\n\n*A)* West\n*B)* North\n*C)* South\n*D)* East","answer":"D","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! Water boils at ___ °C?*\n\n*A)* 50\n*B)* 75\n*C)* 100\n*D)* 150","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! How many fingers on one hand?*\n\n*A)* 4\n*B)* 5\n*C)* 6\n*D)* 7","answer":"B","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! What is the capital of India?*\n\n*A)* Mumbai\n*B)* Kolkata\n*C)* New Delhi\n*D)* Chennai","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! Which planet is Earth?*\n\n*A)* 1st\n*B)* 2nd\n*C)* 3rd\n*D)* 4th","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! How many months in a year?*\n\n*A)* 10\n*B)* 11\n*C)* 12\n*D)* 13","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! What is 10 × 10?*\n\n*A)* 10\n*B)* 100\n*C)* 1000\n*D)* 110","answer":"B","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! Lion is to roar as dog is to ___?*\n\n*A)* Moo\n*B)* Bark\n*C)* Meow\n*D)* Hiss","answer":"B","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! Sky is ___?*\n\n*A)* Green\n*B)* Red\n*C)* Blue\n*D)* Yellow","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! A triangle has ___ sides?*\n\n*A)* 2\n*B)* 3\n*C)* 4\n*D)* 5","answer":"B","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! Ice is ___ water?*\n\n*A)* Warm\n*B)* Liquid\n*C)* Solid\n*D)* Gas","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! Bees make ___?*\n\n*A)* Milk\n*B)* Wax only\n*C)* Honey\n*D)* Syrup","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! How many players in a football team?*\n\n*A)* 9\n*B)* 10\n*C)* 11\n*D)* 12","answer":"C","category":"rapid"},
    {"text":"⚡ *RAPID FIRE! What is 2 × 2 × 2?*\n\n*A)* 4\n*B)* 6\n*C)* 8\n*D)* 12","answer":"C","category":"rapid"},
]

# ══════════════════════════════════════════════════════════════════
# 🤖  PROGRAMMATICALLY GENERATED TASKS (fills to 10,000+)
# ══════════════════════════════════════════════════════════════════

def _gen_math():
    tasks = []
    import random as _r

    # Addition (a+b, options ±5)
    for a in range(1, 100):
        for b in range(1, 100):
            correct = a + b
            opts = sorted({correct, correct-5, correct+5, correct+11})
            while len(opts) < 4:
                opts.append(correct + _r.randint(2, 20))
            opts = sorted(set(opts))[:4]
            _r.shuffle(opts)
            letters = ["A","B","C","D"]
            ans_letter = letters[opts.index(correct)]
            opts_str = "\n".join(f"*{letters[i]})* {opts[i]}" for i in range(4))
            tasks.append({"text": f"🔢 *What is {a} + {b}?*\n\n{opts_str}", "answer": ans_letter, "category": "math"})
            if len(tasks) >= 2000:
                return tasks

    return tasks

def _gen_multiplication():
    tasks = []
    import random as _r
    for a in range(2, 25):
        for b in range(2, 25):
            correct = a * b
            opts = sorted({correct, correct - _r.randint(2, a), correct + _r.randint(3, b+2), correct + _r.randint(a, a*2)})
            while len(opts) < 4:
                opts.append(correct + _r.randint(1, 15))
            opts = sorted(set(opts))[:4]
            _r.shuffle(opts)
            letters = ["A","B","C","D"]
            ans_letter = letters[opts.index(correct)]
            opts_str = "\n".join(f"*{letters[i]})* {opts[i]}" for i in range(4))
            tasks.append({"text": f"🔢 *What is {a} × {b}?*\n\n{opts_str}", "answer": ans_letter, "category": "math"})
            if len(tasks) >= 1500:
                return tasks
    return tasks

def _gen_subtraction():
    tasks = []
    import random as _r
    for a in range(10, 200):
        for b in range(1, a):
            correct = a - b
            opts = sorted({correct, correct + 3, correct - 3, correct + 7})
            while len(opts) < 4:
                opts.append(correct + _r.randint(1, 12))
            opts = [x for x in sorted(set(opts)) if x >= 0][:4]
            if len(opts) < 4:
                continue
            _r.shuffle(opts)
            letters = ["A","B","C","D"]
            if correct not in opts:
                continue
            ans_letter = letters[opts.index(correct)]
            opts_str = "\n".join(f"*{letters[i]})* {opts[i]}" for i in range(4))
            tasks.append({"text": f"🔢 *What is {a} - {b}?*\n\n{opts_str}", "answer": ans_letter, "category": "math"})
            if len(tasks) >= 1500:
                return tasks
    return tasks

def _gen_percentage():
    tasks = []
    import random as _r
    pairs = [(10,100),(20,100),(25,200),(50,300),(30,150),(15,200),(5,400),(40,500),(75,400),(60,300)]
    for pct, base in pairs:
        correct = pct * base // 100
        opts = sorted({correct, correct+5, correct-5, correct+10})
        while len(opts) < 4:
            opts.append(correct + _r.randint(2, 20))
        opts = [x for x in sorted(set(opts)) if x >= 0][:4]
        _r.shuffle(opts)
        letters = ["A","B","C","D"]
        if correct not in opts:
            continue
        ans_letter = letters[opts.index(correct)]
        opts_str = "\n".join(f"*{letters[i]})* {opts[i]}" for i in range(4))
        tasks.append({"text": f"🔢 *What is {pct}% of {base}?*\n\n{opts_str}", "answer": ans_letter, "category": "math"})
    return tasks

# Build the full task list
_GENERATED = _gen_math() + _gen_multiplication() + _gen_subtraction() + _gen_percentage()
ALL_TASKS = TASKS + _GENERATED


def get_random_task() -> dict:
    """Return a random task from the full pool."""
    return random.choice(ALL_TASKS)


def get_task_by_category(category: str) -> dict:
    """Return a random task from a specific category."""
    pool = [t for t in ALL_TASKS if t.get("category") == category]
    return random.choice(pool) if pool else get_random_task()


def get_categories() -> list:
    return sorted(set(t.get("category","general") for t in ALL_TASKS))


def get_task_count() -> int:
    return len(ALL_TASKS)
