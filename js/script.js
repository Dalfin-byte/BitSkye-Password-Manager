function getRandomInt(max) {
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    return array[0] % max;
  }

  function generatePassword(length, includeUppercase, includeLowercase, includeDigits, includeSymbols, excludeAmbiguous, excludeChars) {
    const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const lowercase = 'abcdefghijklmnopqrstuvwxyz';
    const digits = '0123456789';
    const symbols = '!@#$%^&*()_+[]{}|;:,.<>?';
    const ambiguous = 'O0Il';

    let charPool = '';
    if (includeUppercase) charPool += uppercase;
    if (includeLowercase) charPool += lowercase;
    if (includeDigits) charPool += digits;
    if (includeSymbols) charPool += symbols;
    if (excludeAmbiguous) charPool = charPool.split('').filter(c => !ambiguous.includes(c)).join('');
    if (excludeChars) charPool = charPool.split('').filter(c => !excludeChars.includes(c)).join('');

    if (!charPool) return 'Error: No character set selected!';

    let password = '';
    const crypto = window.crypto || window.msCrypto;
    for (let i = 0; i < length; i++) {
      const randomIndex = crypto.getRandomValues(new Uint32Array(1))[0] % charPool.length;
      password += charPool[randomIndex];
    }
    return password;
  }

  function generatePassphrase(wordCount) {
    const wordList = ['apple', 'banana', 'cherry', 'dog', 'elephant', 'flower', 'guitar', 'house', 'island', 'jungle'];
    const crypto = window.crypto || window.msCrypto;
    const passphrase = [];
    for (let i = 0; i < wordCount; i++) {
      const randomIndex = crypto.getRandomValues(new Uint32Array(1))[0] % wordList.length;
      passphrase.push(wordList[randomIndex]);
    }
    return passphrase.join('-');
  }

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

  function escapeHtml(text) {
    const map = {
      '<': '&lt;',
      '>': '&gt;',
      '&': '&amp;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[<>&"'']/g, function(m) { return map[m]; });
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    const lengthSlider = document.getElementById("lengthSlider");
    const lengthValue = document.getElementById("lengthValue");
    const upperCaseToggle = document.getElementById("upperCaseToggle");
    const lowerCaseToggle = document.getElementById("lowerCaseToggle");
    const digitsToggle = document.getElementById("digitsToggle");
    const punctuationToggle = document.getElementById("punctuationToggle");
    const excludeAmbiguousToggle = document.getElementById("excludeAmbiguousToggle");
    const excludeChars = document.getElementById("excludeChars");
    const passphraseToggle = document.getElementById("passphraseToggle");
    const wordCount = document.getElementById("wordCount");
    const multipleCount = document.getElementById("multipleCount");
    const generateBtn = document.getElementById("generateBtn");
    const passwordList = document.getElementById("passwordList");
    const strengthSection = document.getElementById("strengthSection");

    // Update the displayed length value
    lengthSlider.addEventListener("input", function () {
      lengthValue.textContent = lengthSlider.value;
    });

    // Generate passwords on button click
    generateBtn.addEventListener("click", () => {
      const length = parseInt(document.getElementById("lengthSlider").value);
      const includeUppercase = document.getElementById("upperCaseToggle").checked;
      const includeLowercase = document.getElementById("lowerCaseToggle").checked;
      const includeDigits = document.getElementById("digitsToggle").checked;
      const includeSymbols = document.getElementById("punctuationToggle").checked;
      const excludeAmbiguous = document.getElementById("excludeAmbiguousToggle").checked;
      const excludeChars = document.getElementById("excludeChars").value;
      const multipleCount = parseInt(document.getElementById("multipleCount").value);

      const passwords = [];
      for (let i = 0; i < multipleCount; i++) {
        passwords.push(
          generatePassword(
            length,
            includeUppercase,
            includeLowercase,
            includeDigits,
            includeSymbols,
            excludeAmbiguous,
            excludeChars
          )
        );
      }

      displayPasswords(passwords);
    });

    // Display passwords in the list
    function displayPasswords(passwords) {
      const passwordList = document.getElementById("passwordList");
      passwordList.innerHTML = "";

      passwords.forEach((password) => {
        const listItem = document.createElement("li");
        listItem.className = "list-group-item d-flex justify-content-between align-items-center";

        const passwordText = document.createElement("span");
        passwordText.textContent = password;

        const copyButton = document.createElement("button");
        copyButton.className = "btn btn-sm btn-secondary";
        copyButton.textContent = "Copy";
        copyButton.addEventListener("click", () => copyToClipboard(password));

        listItem.appendChild(passwordText);
        listItem.appendChild(copyButton);
        passwordList.appendChild(listItem);
      });
    }

    // Copy password to clipboard
    function copyToClipboard(password) {
      const tempInput = document.createElement("input");
      tempInput.value = password;
      document.body.appendChild(tempInput);
      tempInput.select();
      document.execCommand("copy");
      document.body.removeChild(tempInput);
      alert("Password copied to clipboard!");
    }
  });