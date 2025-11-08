# Quick Start - Hardcoded Version

## ✅ Your credentials are already configured!

- **API Key:** `bn-e947064ac0e041948e5fe78a59a5a3c1`
- **Agent ID:** `87f0e234-fa36-45d4-9297-b2097709636d`

Both are hardcoded in the app - no need to enter them manually! 🎉

---

## 🚀 2-Step Setup

### Step 1: Install Dependencies
```bash
pip install streamlit requests
```

### Step 2: Run the App
```bash
streamlit run abandoned_cart_caller.py
```

That's it! The app will open in your browser automatically.

---

## 📞 How to Use

1. Enter customer phone number (with country code)
   - Example: `+919876543210` (for India)
   - Example: `+12125551234` (for USA)

2. Click **"📞 Initiate Call"** button

3. Your Bolna agent will call the customer! ✨

---

## 🧪 Test First!

**Important:** Test with your own number first to make sure everything works:

```
1. Enter your phone number: +91XXXXXXXXXX
2. Click "Initiate Call"
3. You should receive a call from your Bolna agent
4. If successful, start using for customers!
```

---

## 📱 Phone Number Format

Always use international format:
- ✅ **Correct:** `+919876543210`
- ✅ **Correct:** `+12125551234`
- ❌ **Wrong:** `9876543210` (missing + and country code)
- ❌ **Wrong:** `919876543210` (missing +)

---

## 🎯 Example Usage

For an Indian customer:
```
Phone: +919876543210
Click "Initiate Call" ➡️ Done!
```

For a US customer:
```
Phone: +12125551234
Click "Initiate Call" ➡️ Done!
```

---

## ⚠️ Troubleshooting

**"Error initiating call"**
- Check phone number format (must start with +)
- Ensure Bolna agent is active in your dashboard
- Verify you have credits/balance in Bolna account

**Call not connecting**
- Double-check phone number is correct
- Make sure the number can receive calls
- Check Bolna dashboard for call status

---

## 🔒 Security Note

Your API key is hardcoded in the file. If you share this code:
- **Don't** push to public GitHub
- **Don't** share the `abandoned_cart_caller.py` file publicly
- Consider using environment variables for production

---

## 💡 Pro Tips

1. **Test thoroughly** with your own number before using with customers
2. **Check Bolna dashboard** to see call status and logs
3. **Monitor your credits** in Bolna account
4. **Keep your agent prompt updated** for best results

---

## 🆘 Need Help?

- Check Bolna dashboard for call logs
- Review Bolna documentation: https://docs.bolna.dev
- Ensure your agent is properly configured for abandoned cart scenarios

---

## 🎉 You're All Set!

No configuration needed - just run the app and start making calls!

```bash
streamlit run abandoned_cart_caller.py
```

Happy calling! 📞✨