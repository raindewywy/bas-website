# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary (confirmed): Thai TCAS applicants and their parents, choosing a programme and checking tuition, careers and how to apply.

Secondary (confirmed as secondary): current students, faculty and staff, and partners, who come for calendars, forms, services and directories.

## Product Purpose

The public website of the Faculty of Business Administration for Society, Srinakharinwirot University (BAS SWU, คณะบริหารธุรกิจเพื่อสังคม มศว). It helps prospective students understand the faculty, compare programmes and move on to admissions, and serves as the faculty's public record for news, people, quality assurance and sustainability.

Success metrics: undecided.

## Positioning

Business administration for society (confirmed). Philosophy: "Business Education for Sustainable Society" (การบริหารธุรกิจเพื่อความยั่งยืนของสังคม). This is in the faculty's name and is backed by the Social Enterprise programme and sustainability work. International standing (AACSB member since 2566, GBM, overseas partners) and industry collaboration support it rather than lead.

## Operating Context

- Applicants enter through programmes and admissions pages; undergraduate admission runs through TCAS.
- Overseas applicants to GBM apply through an existing Google Form, labelled "Overseas students application (GBM)".
- M.B.A. and Ph.D. cards link out to mba.swu.ac.th.
- Many documents and news items originate on bas.swu.ac.th, bas1 and bas2 and are linked from there.

## Capabilities and Constraints

- Static HTML, CSS and JavaScript with no build step; shared partials are loaded with `fetch`, so pages need http(s).
- Programmes, news, people and clubs render from `assets/data.js`. Operational detail is in `README.md`.
- The catalogue lists 9 programmes: 7 undergraduate, 2 graduate.
- B.B.A. (Hospitality Management) / การจัดการธุรกิจบริการ has two majors: ธุรกิจท่องเที่ยว (Tourism Business) and ธุรกิจโรงแรม (Hotel Business).
- Global Business Management is always shown with "(International Program)", American spelling.
- Programme pages link one programme document, labelled "เอกสารแนะนำหลักสูตร".
- Open: the 2570 Hospitality Management curriculum document shows no University Council approval date; confirm with the faculty.

## Brand Commitments

- English leads, Thai follows as the secondary line (confirmed, binding): headings and main labels are English, small text (subtitles and descriptions) is Thai.
- Name: BAS SWU; Faculty of Business Administration for Society; คณะบริหารธุรกิจเพื่อสังคม.
- Existing logo assets in `assets/media/`, including `brand-logo.png`.

## Evidence on Hand

- AACSB membership, stated as member, not accredited (`about.html`).
- Faculty profiles and CVs (`assets/data.js`, `assets/cv/`), partner list, news and images (`assets/media/`).
- Performance reports and plans (`qa.html`, `about.html#annual-report`); Green Office evidence (`assets/docs/greenoffice/`).
- Alumni videos and club Instagram accounts (`student-life.html`).
- No verified graduate employment rate, salary, ranking or written student testimonial was identified during init; do not invent them.

## Product Principles

1. Put an applicant's or parent's question first; internal services remain easy to reach but secondary.
2. Show business for society through real programmes, people and work rather than slogans alone.
3. English headings lead; Thai small text carries the meaning, so parents are not left with a partial version.
4. Keep names, fees and document labels consistent wherever they appear.

## Accessibility & Inclusion

Audiences read English and Thai. Existing code supports reduced motion, and `README.md` forbids white text on `--brand-500`. A formal conformance target is undecided.
