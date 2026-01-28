# Cherri Returns & Exchange Skill

Handle customer returns and exchanges for Cherri underwear by looking up orders in Shopify, checking eligibility, and generating personalized response emails.

## Quick Start

1. **Get order info** - Extract order # from email or ask customer
2. **Look up in Shopify** - Use MCP tools to get order details
3. **Check eligibility** - Verify against policy (7-day window, flexible)
4. **Generate response** - Use appropriate template below

**Full policy reference:** [returns-policy.md](../../../operations/policies/returns-policy.md)

## Entry Points

### Path A: Returns Portal Form
Customer submitted via returns portal. Email usually contains:
- Order number
- Size preference (bigger/smaller)
- Reason for return

**Action:** Skip asking for info → go straight to Shopify lookup

### Path B: Direct Email
Customer emailed hi@shopcherri.com directly. May need:
- Order number (or email used for order)
- Size preference for replacement

**Action:** Check if order # is present; if not, use Template A

## Shopify Lookup

### Find Order by Number
```
mcp__shopify__listOrders with query: "name:#ORDER_NUMBER"
```

### Find Order by Email
```
mcp__shopify__listCustomers with query: "email:customer@email.com"
mcp__shopify__listOrders with query: "customer_id:CUSTOMER_ID"
```

### Get Order Details
```
mcp__shopify__getOrder with id: "gid://shopify/Order/ORDER_ID"
```

### Check Stock Availability
```
mcp__shopify__listProducts with query: "PRODUCT_NAME"
```

### Key Order Fields to Check:
- `fulfillments` → delivery date from tracking
- `lineItems` → products ordered (name, variant, quantity)
- `tags` → may include "Order Protection" or similar
- `customer` → order history count
- `createdAt` → order date (use delivery date for window, not this)

## Eligibility Quick Check

| Check | Pass | Fail |
|-------|------|------|
| Order # found? | Continue | Template A |
| Within 7 days of delivery? | Continue | Check exceptions |
| Has valid exception? | Continue | Template E |
| Damage/lost claim + Order Protection? | Template G | - |
| Damage/lost claim, no Order Protection? | Case-by-case | Template H |
| Stock available? | Continue | Template F |

**Exceptions to approve:** Loyal customer, first-time buyer, valid reason, polite tone

## Item Condition Actions

| Condition | Replacement | Return Label |
|-----------|-------------|--------------|
| Unopened | Yes | Yes |
| Opened/Tried on | Yes | Yes |
| Worn | Yes | No |

## Response Templates

### Template A: Need Order Number
```
Subject: Re: [Original Subject]

Hi [Name],

Thanks for reaching out! I'd be happy to help with your exchange.

Could you please share your order number? You can find it in your confirmation email - it starts with a # followed by numbers.

Alternatively, let me know the email address you used when placing the order and I can look it up for you.

Talk soon,
[Your name]
Cherri
```

### Template B: Need Size Preference
```
Subject: Re: [Original Subject]

Hi [Name],

Thanks for reaching out about your order #[ORDER]!

I can see you ordered [PRODUCT] in size [SIZE]. I'd love to help you exchange for a better fit.

What size would you like instead? If you're not sure, let me know what the fit issue was (too tight, too loose, etc.) and I can help recommend the right size.

Looking forward to getting you sorted!

[Your name]
Cherri
```

### Template C: Approved - Return Label Needed
```
Subject: Re: [Original Subject]

Hi [Name],

Great news - your exchange is approved!

Here's the plan:
1. I'm sending your new [PRODUCT] in size [NEW_SIZE] right away
2. Please send back the original item using the prepaid return label I'll include with your package
3. Just pop the original in any mailbox and you're done!

Your new item should arrive within [X] business days.

Let me know if you have any questions!

[Your name]
Cherri
```

### Template D: Approved - No Return Needed (Worn Item)
```
Subject: Re: [Original Subject]

Hi [Name],

No worries at all - I totally get it!

I'm sending your replacement [PRODUCT] in size [NEW_SIZE] right now. Since you've already worn the original, no need to send it back - consider it yours to keep or pass along to someone who might love it.

Your new item should arrive within [X] business days.

Enjoy!

[Your name]
Cherri
```

### Template E: Declined - Past Window
```
Subject: Re: [Original Subject]

Hi [Name],

Thanks for reaching out about your order #[ORDER].

I took a look and it looks like this order was delivered on [DATE], which is outside our 7-day exchange window. I'm really sorry I can't process an exchange for this one.

If there's anything else I can help with, or if you'd like to place a new order, I'm happy to assist!

[Your name]
Cherri
```

### Template F: Out of Stock
```
Subject: Re: [Original Subject]

Hi [Name],

Thanks for reaching out about exchanging your [PRODUCT]!

I checked our inventory and unfortunately size [SIZE] is currently out of stock. Let me double-check if we have any extra stock available and I'll get back to you shortly.

In the meantime, here are some alternatives:
- [ALTERNATIVE 1] in size [SIZE] - similar style
- [ALTERNATIVE 2] - different color in your size
- Store credit to use when [SIZE] is back in stock

Let me know what sounds best to you!

[Your name]
Cherri
```

### Template G: Order Protection Claim
```
Subject: Re: [Original Subject]

Hi [Name],

I'm so sorry to hear about [issue: your package being lost/damaged/stolen]!

Good news - you have Order Protection on this order, which covers exactly this situation.

Here's what to do:
1. Go to orderprotection.com
2. Use your order confirmation email to file a claim
3. They'll take care of getting you a replacement or refund

The process is usually pretty quick. If you run into any issues with the claim, let me know and I'll help however I can!

[Your name]
Cherri
```

### Template H: Damage Claim - No Order Protection
```
Subject: Re: [Original Subject]

Hi [Name],

I'm really sorry to hear your [PRODUCT] arrived [damaged/defective]! That's definitely not the experience we want for you.

I looked into your order and while you don't have Order Protection, I want to make this right. I'm happy to send you a replacement [PRODUCT] - no need to return the damaged one.

Just confirm the size you'd like and I'll get it shipped out today.

[Your name]
Cherri
```

### Template I: Sizing Guidance
```
Subject: Re: [Original Subject]

Hi [Name],

Happy to help you figure out the right size!

You ordered [PRODUCT] in size [SIZE] and mentioned [ISSUE]. Based on that, I'd recommend going [up/down] to size [NEW_SIZE].

Here's my thinking: [brief explanation - e.g., "Since you mentioned the band felt tight but the cups were fine, going up one band size should give you more room while keeping the same cup fit."]

Does that sound good? Let me know and I'll get your exchange started!

[Your name]
Cherri
```

## Workflow Checklist

- [ ] Order number obtained
- [ ] Order looked up in Shopify
- [ ] Delivery date verified
- [ ] Eligibility confirmed (or exception approved)
- [ ] Item condition determined
- [ ] Replacement stock checked
- [ ] Response email drafted
- [ ] Return label generated (if needed) from Shopify order page

## Quick Commands

**Look up order:**
> "Look up Cherri order #12345"

**Check customer history:**
> "How many orders has customer@email.com placed?"

**Check product stock:**
> "Is [product name] size [size] in stock?"

**Generate response:**
> "Draft an exchange approval email for [scenario]"

## Post-Approval Steps

After approving an exchange:

1. **Generate return label** (if needed)
   - Go to Shopify admin → Orders → [Order #]
   - Click "More actions" → "Create return label"

2. **Create replacement order** (or manual ship from inventory)
   - Note: Process depends on Cherri's fulfillment setup

3. **Update order notes**
   - Add note about exchange: size change, reason, any exceptions made

## Escalation

Escalate to team lead when:
- Customer is threatening or abusive
- Claim amount is unusually high
- Multiple items in dispute
- Customer claims fraud or unauthorized purchase
- You're genuinely unsure what to do

## Brand Voice Reminders

- Warm and friendly, not corporate
- Use "I" not "we" when possible
- Casual but professional
- Empathetic - acknowledge frustration
- Solution-focused - always offer a path forward
