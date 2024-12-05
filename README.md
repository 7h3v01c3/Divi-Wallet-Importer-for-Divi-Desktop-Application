## Divi Wallet Importer for Divi Desktop

The **Divi Wallet Importer** is a GUI application designed to allow users to securely import their 12-word mnemonic seed phrase from Divi Wallet Mobile into the Divi Desktop Application. This facilitates seamless access and control over Divi funds on the desktop. The application is in its initial version and is primarily developed to support migration from Divi Labs' mobile wallet to Divi Foundation's Desktop Application (core blockchain application).

### Features

- **Mnemonic Seed Phrase Import**: Supports 12-word mnemonic phrases, adhering to the BIP39 standard for secure phrase verification.
- **Automatic Backup**: Ensures the safety of existing `wallet.dat` files by backing them up before any new wallet imports.
- **User-Friendly Interface**: Developed with CustomTkinter, the app offers a familiar look, similar to the Divi Desktop Application, and a straightforward seed import process.
- **Logging and Troubleshooting**: Error logs are stored on the user's Desktop under the `DWtoDD_logs` folder, enabling easy troubleshooting.
- **Error Handling**: Built-in error handling ensures that any issues encountered during the recovery process are managed smoothly.
- **Dependencies**: Utilizes several Python packages, including `psutil`, `Pillow`, `customtkinter`, and `mnemonic`.

### Installation

1. **Download the Application**: Visit the **Releases** section on this GitHub repository to download the latest compiled `.exe` for Windows or `.app` for macOS (coming soon).
2. **Running on Windows**:
   - After downloading, double-click the `.exe` file to run the application.
   - Or install the `msi` and click the shortcut on desktop to run the application.
   - Windows Defender or Firewall may display a prompt; please allow the application to run.
3. **macOS and Future Versions**:
   - The macOS `.app` version is currently under development and will be released shortly.
   - The `.msix` package for Windows in Microsoft store and cross-platform versions may also be available in future updates.

### Easy Steps

# The steps easy peasy recovery flow, is best on a new desktop install, or better if you also want to migrate choose a second machine and recover.

1. **Install Divi Desktop**: If Divi Desktop is not installed, install Divi Desktop Application on your computer first.
2. **Sync Divi Desktop**: Allow Divi Desktop to fully sync with the blockchain. This step may take some time.
3. **Shutdown Divi Desktop**: Once it’s fully synced, close the Divi Desktop application.
4. **Run Divi Wallet Importer**: Launch Divi Wallet Importer and follow the steps it provides for the migration process. 
5. **Be Patient**: Though the migration process is fast, the Divi Desktop portion may take a while to complete  loading, and synchronizing until fully synced.
6. **Close Encrypt Wallet**: Once the "encrypt wallet" pop up notification appears, close the the pop up (wait to encrypt).
7. **Inspect Your Balance**: Open Divi Desktop and confirm that your balance has been successfully migrated.
8. **Close Divi Desktop**: Once you’ve confirmed the balance, shut down the Divi Desktop application again.
9. **Restart Divi Desktop**: Open the Divi Desktop application once more.
10. **Set a Password**: Click on the black triangle icon, and set a password to encrypt your wallet.

> **⚠️ Important Note:**  
> Seed words displayed in Divi Wallet are uppercase. However, the core engine will only regenerate your wallet correctly if they are entered in lowercase. Ensure you enter your seed words in lowercase.


Lastly, **Uninstall the Divi Wallet Importer**: After completing these steps, you won’t need the app again, so you can uninstall it from your system.

### High Level Overview
1. **Run the Application**: Launch the application and follow the on-screen instructions.
2. **Input Mnemonic Phrase**: Enter your 12-word seed phrase, and the app will validate it.
3. **Backup Existing Wallet**: If a `wallet.dat` file is detected, the app will prompt you to create a backup before proceeding.
4. **Monitor Recovery**: After the seed phrase is validated, the recovery process will begin. The application will notify you of progress through messages and an animated loading icon.
5. **Access Divi Desktop**: Once recovery is complete, Divi Desktop will launch automatically for you to access your recovered wallet.

### Dependencies

- **Python Packages**: This application relies on the following packages, which should be installed in your Python environment:
  - `psutil`
  - `Pillow`
  - `customtkinter`
  - `mnemonic`

These can be installed via `pip`:

```bash
pip install psutil pillow customtkinter mnemonic
```

### Notes

- **Experimental Release**: This is an experimental version. Please report any issues on the GitHub repository's **Issues** section.
- **Multi-Platform Compatibility**: While separate versions are currently available for Windows and macOS, a cross-platform version that includes Linux support is being considered for future releases.

### Troubleshooting

- **Error Logs**: If you encounter any issues, refer to the `DWtoDD_logs` directory on your Desktop. These logs can provide insights for troubleshooting.
- **Known Issues**:
  - Console Window on Windows: Some users may experience a brief console window popup when running certain recovery operations. This is addressed by suppressing the console as much as possible within the code.

### Contributing

We welcome contributions! Please fork this repository and submit pull requests for any bug fixes or enhancements. Make sure to adhere to best coding practices and provide clear documentation for any changes.

For questions, feature requests, or bug reports, please visit the Issues section.

---

Thank you for using the **Divi Wallet Importer for Divi Desktop**!
