<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ShoeMetrics Engineering - Integrated System</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
        :root {
            --primary: #3b82f6; --success: #10b981; --warning: #f59e0b; 
            --danger: #ef4444; --bg: #0f172a; --card: #1e293b; --text: #f8fafc; --female: #ec4899;
            --twitter-border: rgba(255,255,255,0.1);
        }
        * { box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; transition: all 0.2s ease; }
        body { margin: 0; background: var(--bg); color: var(--text); padding: 0; padding-bottom: 80px; overflow-x: hidden; }
        
        /* BOTTOM NAV */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; right: 0; height: 75px;
            background: rgba(30, 41, 59, 0.95); backdrop-filter: blur(10px);
            border-top: 2px solid var(--twitter-border);
            display: flex; justify-content: space-around; align-items: center; z-index: 1000;
        }
        .nav-item {
            cursor: pointer; display: flex; flex-direction: column; align-items: center;
            color: #94a3b8; font-size: 10px; font-weight: 800; text-transform: uppercase; gap: 5px;
        }
        .nav-item.active { color: var(--primary); }
        .nav-dot { width: 14px; height: 14px; border-radius: 4px; background: #334155; transform: rotate(45deg); }
        .nav-item.active .nav-dot { background: var(--primary); box-shadow: 0 0 15px var(--primary); }

        /* PAGE ANIMATION */
        .page { display: none; padding: 15px; animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
        .page.active { display: block; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

        /* LEARNING MODULE CARDS */
        .module-container { max-width: 1000px; margin: auto; padding-top: 10px; }
        .module-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .m-card { 
            background: var(--card); border-radius: 24px; border: 1px solid var(--twitter-border);
            overflow: hidden; position: relative; transition: 0.3s;
        }
        .m-card:hover { transform: translateY(-10px); border-color: var(--primary); }
        .m-img { width: 100%; height: 180px; object-fit: cover; filter: grayscale(40%) contrast(1.1); }
        .m-content { padding: 20px; }
        .m-tag { font-size: 9px; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 1px; }
        .m-title { font-size: 18px; font-weight: 800; margin: 8px 0; color: white; }
        .m-text { font-size: 13px; color: #94a3b8; line-height: 1.6; }

        /* SYSTEM CORE STYLES (KEEPING EVERYTHING) */
        .app-container { background: var(--card); border-radius: 28px; overflow: hidden; border: 1px solid var(--twitter-border); box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
        .header { padding: 20px; text-align: center; background: rgba(0,0,0,0.3); border-bottom: 1px solid var(--twitter-border); }
        .main-content { display: flex; flex-direction: column; }
        @media (min-width: 992px) { .main-content { flex-direction: row; } }
        .sidebar { flex: 1; padding: 20px; background: rgba(255,255,255,0.02); border-right: 1px solid var(--twitter-border); }
        .display-area { flex: 1.5; padding: 20px; background: var(--card); }
        .field { margin-bottom: 12px; }
        label { font-size: 10px; font-weight: 800; color: #94a3b8; text-transform: uppercase; display: block; margin-bottom: 5px; }
        input, select { width: 100%; background: #0f172a; border: 2px solid #334155; border-radius: 12px; font-size: 13px; color: white; padding: 12px; outline: none; }
        .gender-selector { display: flex; gap: 10px; margin-bottom: 15px; }
        .gender-btn { flex: 1; padding: 10px; border-radius: 10px; border: 2px solid #334155; background: #0f172a; color: #94a3b8; cursor: pointer; font-weight: 800; font-size: 11px; text-align: center; }
        .gender-btn.active.male { border-color: var(--primary); color: var(--primary); background: rgba(59,130,246,0.1); }
        .gender-btn.active.female { border-color: var(--female); color: var(--female); background: rgba(236,72,153,0.1); }
        .dashboard { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
        @media (max-width: 768px) { .dashboard { grid-template-columns: repeat(2, 1fr); } }
        .tile { background: rgba(255,255,255,0.03); padding: 12px; border-radius: 18px; text-align: center; border: 1px solid var(--twitter-border); }
        .tile-label { font-size: 9px; color: #94a3b8; font-weight: 800; text-transform: uppercase; }
        .tile-val { font-size: 18px; font-weight: 800; color: var(--primary); display: block; margin-top: 4px; }
        .tech-sheet { background: rgba(0,0,0,0.3); border-radius: 20px; padding: 15px; overflow-x: auto; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; min-width: 480px; }
        th { text-align: left; padding: 10px; color: var(--primary); border-bottom: 1px solid #334155; text-transform: uppercase; font-size: 10px; }
        td { padding: 10px; border-bottom: 1px solid var(--twitter-border); color: var(--text); }
        .brand-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px; }
        .brand-card { background: rgba(255,255,255,0.05); padding: 12px; border-radius: 15px; text-align: center; border: 1px solid var(--twitter-border); }
        .brand-n { font-size: 9px; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
        .brand-s { font-size: 14px; font-weight: 800; color: var(--text); display: block; margin-top: 4px; }
        .btn { border: none; padding: 15px; border-radius: 12px; cursor: pointer; font-weight: 800; width: 100%; margin-top: 10px; background: var(--success); color: white; text-transform: uppercase; font-size: 12px; box-shadow: 0 4px 0 #059669; }
        .badge { background: rgba(59,130,246,0.1); color: var(--primary); padding: 2px 6px; border-radius: 4px; font-weight: bold; }
        .comp-box { background: rgba(59,130,246,0.05); border: 1px solid rgba(59,130,246,0.2); padding: 12px; border-radius: 15px; margin-top: 10px; font-size: 11px; }
        #customerHeader { display: none; border-left: 5px solid var(--primary); padding-left: 15px; margin-bottom: 20px; }
    </style>
</head>
<body>

<div id="page1" class="page active">
    <div class="app-container">
        <div class="header">
            <h3 style="margin:0">SHOEMETRICS <span style="color:var(--primary)">ENGINEERING</span></h3>
            <span style="font-size: 10px; color: var(--success)">ATK YOGYAKARTA STANDARDS | INTEGRATED PRODUCTION</span>
        </div>

        <div class="main-content">
            <div class="sidebar">
                <div class="field">
                    <label>👤 Gender</label>
                    <div class="gender-selector">
                        <div id="btnMale" class="gender-btn active male" onclick="setGender('male')">MEN</div>
                        <div id="btnFemale" class="gender-btn female" onclick="setGender('female')">WOMEN</div>
                    </div>
                </div>
                <div class="field"><label>🏷️ Customer</label><input type="text" id="inName" placeholder="Nama Project"></div>
                <div class="field"><label>📏 Foot Length (cm)</label><input type="number" id="inCM" oninput="masterCalc()" placeholder="0.0"></div>
                <div class="field"><label>⭕ Ball Girth (cm)</label><input type="number" id="inGirth" oninput="masterCalc()" placeholder="0.0"></div>
                
                <div class="field">
                    <label>👞 Shoe Style</label>
                    <select id="inStyle" onchange="masterCalc()">
                        <optgroup label="Men / Universal">
                            <option value="1.5" selected>Sport / Sneakers (+15mm)</option>
                            <option value="1.0">Oxford / Casual (+10mm)</option>
                            <option value="0.3">Mocasin / Loafer (+3mm)</option>
                            <option value="2.0">Safety Boots (+20mm)</option>
                        </optgroup>
                        <optgroup label="Women Special">
                            <option value="0.4">Pumps / Stiletto (+4mm)</option>
                            <option value="0.6">Balerina / Flats (+6mm)</option>
                            <option value="0.8">Wedges / Platform (+8mm)</option>
                        </optgroup>
                    </select>
                </div>

                <div class="field">
                    <label>📐 Toe Shape</label>
                    <select id="inToe" onchange="masterCalc()">
                        <option value="1.0">Square Toe (+0mm)</option>
                        <option value="1.1" selected>Round Toe (+1mm)</option>
                        <option value="2.5">Pointy Toe / Lancip (+2.5mm)</option>
                        <option value="1.8">Almond Toe (+1.8mm)</option>
                    </select>
                </div>

                <div class="field"><label>👠 Heel Height (Hak cm)</label><input type="number" id="inHeel" value="0" oninput="masterCalc()"></div>

                <div class="field">
                    <label>⚙️ Production System</label>
                    <select id="inConst" onchange="masterCalc()">
                        <option value="0.01">Cementing (1%)</option>
                        <option value="0.04">Vulcanized (4%)</option>
                        <option value="0.02" selected>Direct Injection (2%)</option>
                    </select>
                </div>

                <div class="field">
                    <label>🧵 Material Detail</label>
                    <select id="inMat" onchange="masterCalc()">
                        <option value="0.6">Cow Leather (Grain)</option>
                        <option value="0.4">Suede / Nubuck</option>
                        <option value="0.45">Mesh (Sandwich)</option>
                        <option value="2.5">Flyknit / Knit</option>
                        <option value="1.5">Synthetic PU</option>
                    </select>
                </div>

                <div class="comp-box">
                    <b style="color:var(--primary); text-transform:uppercase; font-size:9px;">Industrial Analysis:</b><br>
                    <span id="constDesc">Siap menghitung spesifikasi...</span>
                </div>
                <button class="btn" onclick="downloadPDF()">📥 DOWNLOAD PDF</button>
            </div>

            <div class="display-area" id="pdfArea">
                <div id="customerHeader">
                    <h2 id="pdfCustomer" style="margin:0; text-transform: uppercase; color: #3b82f6;">PROJECT NAME</h2>
                    <small id="pdfDate" style="color: #94a3b8;"></small>
                </div>

                <div class="dashboard">
                    <div class="tile"><span class="tile-label">EU Size</span><span id="resEU" class="tile-val">-</span></div>
                    <div class="tile"><span class="tile-label">Mold Length</span><span id="resMold" class="tile-val">-</span></div>
                    <div class="tile"><span class="tile-label">Bottom Width</span><span id="resWidth" class="tile-val" style="color:var(--warning)">-</span></div>
                    <div class="tile"><span class="tile-label">Allowance</span><span id="resAllw" class="tile-val" style="color:var(--success)">-</span></div>
                </div>

                <label>📋 Engineering Specification</label>
                <div class="tech-sheet">
                    <table>
                        <thead><tr><th>Point</th><th>Raw Value</th><th>Final Eng.</th><th>Standard</th></tr></thead>
                        <tbody>
                            <tr><td>Vamp (V)</td><td id="vampRaw">-</td><td id="vampVal" class="badge">-</td><td>7/10 SL</td></tr>
                            <tr><td>Joint (J)</td><td id="jointRaw">-</td><td id="jointVal" class="badge">-</td><td>2/3 SL</td></tr>
                            <tr><td>Instep (I)</td><td id="instepRaw">-</td><td id="instepVal" class="badge">-</td><td>1/2 SL</td></tr>
                            <tr><td>Counter (H)</td><td id="counterRaw">-</td><td id="counterVal" class="badge">-</td><td>Standard Adj</td></tr>
                            <tr><td><b>Target Girth Mold</b></td><td id="gRaw">-</td><td id="gFin" class="badge" style="background:var(--primary); color:white;">-</td><td id="girthStd">-</td></tr>
                        </tbody>
                    </table>
                </div>

                <label>✂️ Manufacturing Process</label>
                <div class="tech-sheet">
                    <table>
                        <thead><tr><th>Process</th><th>Standard</th><th>Machine Required</th></tr></thead>
                        <tbody>
                            <tr><td>Underlay Skiving</td><td>10 mm</td><td>Skiving Machine</td></tr>
                            <tr><td>Folding Margin</td><td>5 mm</td><td>Folding Machine</td></tr>
                            <tr><td>Lasting Margin</td><td>20 mm</td><td>Pincer / Lasting</td></tr>
                            <tr><td>Bottom 
