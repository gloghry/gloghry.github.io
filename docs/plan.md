# Design and launch plan

## Agreed direction

- Garett Loghry: current engineering tools/application work, with some embedded and low-level development. Moving toward embedded systems and firmware.
- Garett is applying to WSU’s engineering and technology management master’s program; do not describe him as enrolled or holding the degree.
- Professional homepage with Projects, Writing, About; résumé follows approved source content.
- Technical posts first. Personal writing may be added later.
- Minimalist centered layout. Nathan Spelts's screenshot is a layout reference; identity and palette are original.
- Atkinson Hyperlegible Next is the primary self-hosted typeface; code remains monospaced.
- Slate/teal themes; avoid hard-to-read dark blue, dark red, and magenta on dark backgrounds. Light neutral body and secondary text in dark mode.
- Follow OS theme initially; remember explicit theme selection. Underline links and show keyboard focus.
- Public contact is contact@garettloghry.com, approved by Garett with receiving and forwarding tested. Sending/replies remain unconfirmed in #34. GitHub and Garett's approved LinkedIn profile (https://www.linkedin.com/in/gloghry/) are linked. Do not use the old email from the Vim file.
- Garett purchased garettloghry.com as the primary domain. DNS, Pages settings, HTTPS, and redirect verification are tracked in #21; see [domain setup](domain.md).
- Analytics remain disabled.

## Content decisions still needed

- Access to résumé repo and approval of public experience/skills details (#11, #12).
- Real projects and permitted source material (#13).
- Remaining mailbox setup checks are tracked in #34; public email and LinkedIn are approved.
- First technical article topic (#15).
- Review colors in the browser and tune to Garett's reading comfort (#3, #10).

## Delivery order

1. Foundation, themes, page skeletons, README, build workflow (#1–#8).
2. Accurate résumé/project content and first technical writing (#11–#15).
3. Responsive/accessibility audits, metadata/feed refinement, favicon, 404/link and performance review (#9, #10, #16–#20).
4. Enable Pages Actions source, merge, and verify deployment (#8).

## Launch checklist

- [ ] Build and internal-link checks pass in GitHub Actions.
- [ ] Test light/dark and system theme, storage unavailable, and keyboard navigation.
- [ ] Check phone/tablet/desktop layouts and article code blocks.
- [ ] Garett approves biography and public links.
- [ ] Add approved résumé/project content before promoting the portfolio.
- [ ] Confirm Pages source, deployment result, and live URL.

The first skeleton has honest empty states and no invented work history or posts. Foundation implementation does not complete content or manual audit issues.

## Page structure and link placement

Each area has a specific job; an existing row of links is not a reason to put another link there.

| Area | Job |
| --- | --- |
| Header | Navigate the site: name/home, Projects, Writing, About, theme control. |
| Homepage introduction | Explain who Garett is and offer one main next step. About me stands alone until real project write-ups exist; then View projects leads, with About as a quieter secondary link. |
| Homepage work sections | Show actual projects and writing, with relevant detail/source links. Hide empty homepage sections; index pages retain honest empty states. |
| About | Background, interests, experience, and relevant professional profiles. Résumé links follow approved content under #12. |
| Contact | A brief invitation and the full, copyable public email address near the bottom of the homepage. |
| Footer | Consistent access to full email address, GitHub, and LinkedIn from every page. Copyright notice follows the rights/notice decisions in #49. |
| Writing | Articles and an RSS subscription link in their reading context. |

Use links for navigation/downloads/email and buttons for actions such as the theme control. Keep internal and external navigation in the same tab by default. Profile links use plain, consistent labels without external-arrow decoration; never use an external-arrow symbol for an internal About link. Keep the full email visible with a mailto destination. Links retain underlines, hover changes, and keyboard-focus outlines, so color is not the only cue.
