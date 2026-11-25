---
name: BAS SWU
description: A clear, trustworthy, friendly bilingual system for the Faculty of Business Administration for Society.
colors:
  campus-sky: "#00A8D0"
  campus-cyan: "#00B3C9"
  campus-link: "#00738F"
  prasarnmit-navy: "#063047"
  deep-campus: "#054966"
  open-sky: "#58C9E4"
  sky-wash: "#EFF9FB"
  apply-yellow: "#FAC315"
  apply-yellow-light: "#FFD54A"
  graduate-purple: "#493B97"
  news-red: "#EF402C"
  paper: "#FBFCFD"
  paper-dim: "#F1F5F6"
  surface: "#FFFFFF"
  ink: "#0F1719"
  ink-soft: "#2A3639"
  muted: "#51636A"
  line: "#D6DEE1"
  line-soft: "#E3E9EB"
typography:
  display:
    fontFamily: "'IBM Plex Sans', 'IBM Plex Sans Thai', sans-serif"
    fontSize: "clamp(2.1rem, 1.6rem + 2.2vw, 3.4rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "'IBM Plex Sans', 'IBM Plex Sans Thai', sans-serif"
    fontSize: "clamp(1.6rem, 1.35rem + 1.4vw, 2.35rem)"
    fontWeight: 700
  title:
    fontFamily: "'IBM Plex Sans', 'IBM Plex Sans Thai', sans-serif"
    fontSize: "17px"
    fontWeight: 700
  body:
    fontFamily: "'IBM Plex Sans Thai', 'IBM Plex Sans', sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.8
  label:
    fontFamily: "'IBM Plex Mono', monospace"
    fontSize: "12px"
    fontWeight: 600
    letterSpacing: "0.14em"
rounded:
  s: "2px"
  chip: "12px"
  panel: "14px"
  card: "16px"
  feature: "20px"
  pill: "999px"
spacing:
  space-1: "0.4rem"
  space-2: "0.8rem"
  space-3: "1.2rem"
  space-4: "1.6rem"
  space-5: "2.4rem"
  space-6: "3.2rem"
  space-7: "4.8rem"
  gutter: "24px"
components:
  button-apply:
    backgroundColor: "{colors.apply-yellow}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0 24px"
    height: "48px"
  button-apply-hover:
    backgroundColor: "{colors.apply-yellow-light}"
  button-outline:
    textColor: "{colors.campus-link}"
    rounded: "{rounded.pill}"
    padding: "0 20px"
    height: "44px"
  button-outline-hover:
    backgroundColor: "{colors.campus-link}"
    textColor: "{colors.surface}"
  button-white:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.prasarnmit-navy}"
    rounded: "{rounded.pill}"
    padding: "0 22px"
    height: "48px"
  filter-chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.pill}"
    padding: "0 18px"
    height: "44px"
  filter-chip-selected:
    backgroundColor: "{colors.prasarnmit-navy}"
    textColor: "{colors.surface}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
  search-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.muted}"
    rounded: "{rounded.pill}"
    padding: "0 16px"
    height: "46px"
---

# Design System: BAS SWU

## Overview

**Creative North Star: "The Open Campus"**

The system feels like a campus that welcomes everyone: airy surfaces, real photographs and clear paths. Its voice is clear, trustworthy and friendly, so applicants and parents can understand a page before they have to study it.

English and Thai share one interface without a language switcher. Sky tones carry wayfinding, navy gives authority, and yellow marks the step toward applying.

**Key Characteristics:**
- Light surfaces with authentic campus imagery.
- English headings; Thai small text beneath them.
- Rounded, easy-to-press controls.
- Flat surfaces that lift when a visitor interacts.

## Colors

Campus sky and deep navy form the world; yellow is the invitation to act.

### Primary
- **Campus Sky** (#00A8D0): brand anchor for icons, strokes, circles and card hover borders; not a text background.
- **Campus Cyan** (#00B3C9): the existing footer, contact, active filter and floating-button field. It is listed as incumbent, with contrast debt below.
- **Campus Link** (#00738F): links, labels and solid fields that carry white text.
- **Open Sky** (#58C9E4): accents and secondary labels on dark fields.
- **Sky Wash** (#EFF9FB): quiet hover and icon backgrounds.

### Secondary
- **Prasarnmit Navy** (#063047): headings, selected programme filters and high-authority fields.
- **Deep Campus** (#054966): secondary dark field.

### Tertiary
- **Apply Yellow** (#FAC315): applying and primary action on dark fields, always with dark ink.
- **Graduate Purple** (#493B97): graduate-level labels only.
- **News Red** (#EF402C): featured-news labels only.

### Neutral
- **Paper** (#FBFCFD), **Dim Paper** (#F1F5F6) and **Surface** (#FFFFFF): page, alternate section and card layers.
- **Ink** (#0F1719), **Soft Ink** (#2A3639) and **Muted** (#51636A): text in descending emphasis.
- **Line** (#D6DEE1) and **Soft Line** (#E3E9EB): control and card boundaries.

### Named Rules
**The White-on-Sky Rule.** Never add white text on Campus Cyan or Campus Sky. White on Campus Cyan measures 2.53:1; use Campus Link instead. Existing footer, contact, active-news-filter and primary detail-page button uses are debt to fix, not precedent.

**The Yellow Invitation Rule.** Reserve Apply Yellow for action and pair it with dark ink.

## Typography

**Display Font:** IBM Plex Sans (with IBM Plex Sans Thai)
**Body Font:** IBM Plex Sans Thai (with IBM Plex Sans)
**Label/Mono Font:** IBM Plex Mono

**Character:** One related family keeps the two scripts coherent. Weight and scale, rather than contrasting typefaces, create authority.

### Hierarchy
- **Display** (700, fluid, 1.1): interior page titles.
- **Headline** (700, fluid): section headings.
- **Title** (700, 17px): links and compact cards; feature cards may be larger.
- **Body** (400, 16px, 1.8): reading copy, up to 62ch.
- **Label** (600, 12px, 0.14em, uppercase): existing English section labels and data accents.

### Named Rules
**The English-Lead Rule.** Headings and main labels are English. Small text is Thai: the subtitle under a heading, descriptions, notes and tags. Do not repeat a description in both languages. The Thai-led homepage hero is marked as a client lock and needs an owner decision before changing.

## Layout

Content sits in a 1280px container with a 24px gutter. Interior sections use fluid vertical spacing of 56-96px. Cards use auto-fit or auto-fill grids with minimums based on content and collapse without horizontal scrolling. The sticky header is 76px high. The implementation uses several responsive breakpoints; 900px and 560px recur most often. On narrow screens navigation becomes a drawer.

## Elevation & Depth

Surfaces are flat at rest, separated by soft borders and alternating paper tones. Shadow mainly acknowledges interaction; dark bands provide larger tonal depth. Some older surfaces still have resting shadows.

### Shadow Vocabulary
- **Small** (`0 1px 2px rgba(15,23,25,.06), 0 1px 1px rgba(15,23,25,.04)`): subtle legacy surface separation.
- **Medium** (`0 10px 28px rgba(15,23,25,.10)`): floating or legacy raised surfaces.
- **Card hover** (`0 20px 40px rgba(6,48,71,.12)`): linked cards on hover.

### Named Rules
**The Flat-at-Rest Rule.** New surfaces are flat by default and lift only in response to interaction.

## Shapes

Controls are capsules (999px). Cards use generously curved corners (16px), document panels 14px, icon tiles 12px and feature surfaces 20px. Circles are used for compact icon controls and brand marks. Thin one-pixel borders define most light cards.

## Components

Components feel rounded, warm and easy to press.

### Buttons
- **Shape:** capsules (999px), generally 44-48px high.
- **Apply:** yellow with dark ink and 24px side padding; lighter yellow on hover.
- **Outline:** Campus Link text and border; fills with Campus Link and white text on hover.
- **White:** white with navy text on dark imagery.
- **Focus:** homepage, header, drawer and footer use a 3px navy outline with a white separation ring.

### Chips
- **Style:** 44px white capsules with a thin border.
- **State:** programme filters select in navy. The homepage news filter currently selects in cyan and falls under the contrast debt.

### Cards / Containers
- **Corner Style:** rounded (16px).
- **Background:** white with a Soft Line border.
- **Shadow Strategy:** flat at rest; linked cards lift 4px on hover.
- **Internal Padding:** commonly 22-24px.

### Inputs / Fields
- **Style:** 46px white search capsule with a 1.5px border.
- **Focus:** border changes to Campus Link; header search also adds a translucent ring.

### Navigation
Sticky, nearly opaque paper bar with a soft bottom border. Desktop uses mega menus; mobile uses a modal drawer whose labels place English over Thai. That bilingual pairing is the reference pattern.

### Document Disclosure
White rounded panels with a tap-friendly summary row, file count, chevron and divided PDF list. Used for reports and transparency documents.

## Do's and Don'ts

### Do:
- **Do** use real campus, student and faculty imagery.
- **Do** use Campus Link (#00738F) behind white text.
- **Do** write headings in English and small text in Thai.
- **Do** reserve Apply Yellow (#FAC315) for action.
- **Do** honor reduced-motion preferences.

### Don't:
- **Don't** put new white text on Campus Cyan (#00B3C9) or Campus Sky (#00A8D0).
- **Don't** introduce another icon library; the site uses Font Awesome.
- **Don't** hardcode a new color when an existing token covers the role.
- **Don't** treat legacy shadows or Thai-led labels as precedent for new work.
