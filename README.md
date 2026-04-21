#  URL Monitoring Extension – Dynatrace Extension Setup Guide

This guide explains how to upload and configure the IBM Storage Insights Dynatrace Extension and set up URL Availability monitoring using Dynatrace Extension 2.0.

---

##  Prerequisites

- Access to Dynatrace GUI  
- ActiveGate installed and running  
- Extension package: `custom_url-availability-0.0.10.zip`  
- Root certificate file: `ca.pem`  

---

##  Step 1: Upload Extension & Configure Certificates

###  Add Certificate to Credential Vault

1. Login to Dynatrace GUI  
2. Navigate to: `Search → Credential Vault`  
3. Click **Add new credential**  
4. Upload the root certificate file [ca.pem](https://github.com/SooryaMuthuraj/URL-Monitoring-Extension/blob/main/certificates/ca.pem) 

---

###  Copy Certificate to ActiveGate

Copy the `ca.pem` file to the ActiveGate machine:

####  Linux
   /var/lib/dynatrace/remotepluginmodule/agent/conf/certificates

####  Windows

%ProgramData%\dynatrace\remotepluginmodule\agent\conf\certificates

---

###  Upload Extension

1. Go to: `Extensions → Upload custom Extension 2.0`  
2. Upload the file `custom_url-availability-0.0.10.zip`  

---

##  Step 2: Configure URL Availability Monitoring

###  Open Extension

1. Navigate to: `Extensions`  
2. Select: [custom:custom_url-availability-0.0.10](https://github.com/SooryaMuthuraj/URL-Monitoring-Extension/blob/main/dist/custom_url-availability-0.0.10.zip)  

---

###  Setup Monitoring

1. Click **Monitor Remotely**  
2. Choose **Default ActiveGate**  
3. Ensure your ActiveGate is visible  
4. Click **Next**  

---

###  Add Endpoint

1. Click **Add Endpoint**  
2. Provide the following details:  

   - **URL** (Example: `https://apmosys.com`)  
   - **Timeout**  
   - **Schedule Interval**  
   - **SSL Requirement** (Enable/Disable)  

3. Click **Next**  

---

###  Final Configuration

1. Enter a **Monitoring Configuration Label**  
2. Click **Activate**  

---

##  Result

- URL availability monitoring will start  
- Metrics and availability data will be visible in Dynatrace dashboards  
- Alerts can be configured based on failures or response time  

---

##  Notes

- Ensure ActiveGate has network access to the target URLs  
- Verify certificate placement if SSL checks fail  
- Restart ActiveGate if certificates are not picked up  

---

##  Troubleshooting

| Issue | Solution |
|------|----------|
| Extension not visible | Re-upload ZIP and refresh UI |
| SSL errors | Verify `ca.pem` placement |
| Take Restart of EEC|
| No data | Check ActiveGate connectivity |
| Timeout issues | Increase timeout value |

---

##  References

- Dynatrace Extensions 2.0 Documentation  
- ActiveGate Configuration Guide  

---
