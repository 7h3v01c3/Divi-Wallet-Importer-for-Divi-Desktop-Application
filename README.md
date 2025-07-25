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

### Easy Steps to Recovery!

The steps for easy-peasy recovery flow work best on a new desktop installation. If you also want to migrate, consider using a second machine for the recovery process.

1. **Install Divi Desktop**: If Divi Desktop is not installed, download and install the Divi Desktop Application on your computer.
2. **Sync Divi Desktop**: Allow Divi Desktop to fully sync with the blockchain. This step may take some time.
3. **Shutdown Divi Desktop**: Once it’s fully synced, close the Divi Desktop application.
4. **Run Divi Wallet Importer**: Launch Divi Wallet Importer and follow its steps for the migration process.
   * **Enter Seed Words in lowercase.**
5. **Divi Wallet Importer will hand off to Divi Desktop**: After confirming your seed words and creating your wallet, the Importer will notify you that it's closing and that Divi Desktop will now open. This handoff signals that the desktop wallet is now taking over the process and will complete the restoration and syncing.
6. **Be Patient**: Though the migration process is fast, the Divi Desktop portion may take a while to fully load and synchronize.
7. **Close Encrypt Wallet Pop-up**: Once the "Encrypt Wallet" pop-up notification appears, close the pop-up (wait to encrypt for now).
8. **Inspect Your Balance**: Open Divi Desktop and confirm that your balance has been successfully migrated.
9. **Close Divi Desktop**: Once you’ve confirmed the balance, shut down the Divi Desktop application again.
10. **Restart Divi Desktop**: Open the Divi Desktop application once more.
11. **Set a Password**: Click on the black triangle icon and set a password to encrypt your wallet.

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

### UPDATES on OSX
Unfortunately, a native macOS app isn’t going to happen. Developing for macOS proved to be a massive time sink for me, as I worked on this as a volunteer and cannot justify the personal cost to continue investing in this anymore. While the Windows version is a gift to the community, the macOS version is too problematic to finish—thanks to its ecosystem. Unless enough Mac users come forward to help fund further development or get other developers involved, it’s not going to happen. Alternatively, since the code is open source, someone else could fork it and complete it freely. Or you can fork the repo and run it in an IDE like PyCharm or VS Code.

---

Thank you for using the **Divi Wallet Importer for Divi Desktop**!
