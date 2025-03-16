function getRandomInt(max) {
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    return array[0] % max;
  }

  // Generate a password with the specified length and options
  function generatePassword(length, options) {
    let alphabet = "";
    if (options.upper) alphabet += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    if (options.lower) alphabet += "abcdefghijklmnopqrstuvwxyz";
    if (options.digits) alphabet += "0123456789";
    if (options.punctuation) alphabet += "!@#$%^&*()_+[]{}|;:,.<>/?";
    if (alphabet.length === 0) return "No character set selected!";
    let pwd = "";
    for (let i = 0; i < length; i++) {
      const index = getRandomInt(alphabet.length);
      pwd += alphabet[index];
    }
    return pwd;
  }

  // Calculate password entropy (bits)
  function calculateEntropy(length, options) {
    let alphabet = "";
    if (options.upper) alphabet += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    if (options.lower) alphabet += "abcdefghijklmnopqrstuvwxyz";
    if (options.digits) alphabet += "0123456789";
    if (options.punctuation) alphabet += "!@#$%^&*()_+[]{}|;:,.<>/?";
    const n = alphabet.length;
    if (n === 0) return 0;
    return length * Math.log2(n);
  }

  // Evaluate password strength and update the progress bar
  function evaluateStrength(entropy) {
    const strengthBar = document.getElementById("strengthBar");
    const strengthText = document.getElementById("strengthText");
    let strengthPercent = 0;
    let strengthLabel = "";

    if (entropy < 50) {
      strengthPercent = 33;
      strengthLabel = "Weak";
      strengthBar.className = "progress-bar bg-danger";
    } else if (entropy < 80) {
      strengthPercent = 66;
      strengthLabel = "Moderate";
      strengthBar.className = "progress-bar bg-warning";
    } else {
      strengthPercent = 100;
      strengthLabel = "Strong";
      strengthBar.className = "progress-bar bg-success";
    }

    strengthBar.style.width = strengthPercent + "%";
    strengthBar.textContent = strengthPercent + "%";
    strengthText.textContent = `Entropy: ${entropy.toFixed(2)} bits — ${strengthLabel}`;
  }

  function copyToClipboard(password) {
    const tempInput = document.createElement('input');
    tempInput.value = password;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    alert('Password copied to clipboard');
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    const lengthSlider = document.getElementById("lengthSlider");
    const lengthValue = document.getElementById("lengthValue");
    const upperCaseToggle = document.getElementById("upperCaseToggle");
    const lowerCaseToggle = document.getElementById("lowerCaseToggle");
    const digitsToggle = document.getElementById("digitsToggle");
    const punctuationToggle = document.getElementById("punctuationToggle");
    const multipleCount = document.getElementById("multipleCount");
    const generateBtn = document.getElementById("generateBtn");
    const passwordList = document.getElementById("passwordList");
    const strengthSection = document.getElementById("strengthSection");
  
    // Update the displayed length value
    lengthSlider.addEventListener("input", function() {
      lengthValue.textContent = lengthSlider.value;
    });
  
    // Generate passwords on button click
    generateBtn.addEventListener("click", function() {
      const length = parseInt(lengthSlider.value);
      const options = {
        upper: upperCaseToggle.checked,
        lower: lowerCaseToggle.checked,
        digits: digitsToggle.checked,
        punctuation: punctuationToggle.checked
      };
      const count = parseInt(multipleCount.value);
    
      // Clear previous results
      passwordList.innerHTML = "";
    
      // Calculate and display strength for a sample password
      const entropy = calculateEntropy(length, options);
      evaluateStrength(entropy);
      strengthSection.style.display = "block";
    
      // Generate and display the requested number of passwords
      for (let i = 0; i < count; i++) {
        const pwd = generatePassword(length, options);
        const li = document.createElement("li");
        li.className = "list-group-item bg-dark text-light d-flex justify-content-between align-items-center";
        li.innerHTML = `
          <button class="btn btn-secondary btn-sm" onclick="copyToClipboard('${pwd}')">Copy</button>
          <span>${pwd}</span>
        `;
        passwordList.appendChild(li);
      }
    });
  });