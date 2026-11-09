# V317 — FINZANJIR domeni va candidate arxivi auditi

**Manba:** ZIP-2, V317 Semantic Gate + Domain Expansion  
**Maqom:** metadata va matn tuzilmasi auditi; faktik ekspert tasdig‘i emas.

## 1. FINZANJIR domenidagi 188 yozuv

Active index ichida domain=finzanjir bo‘lgan 188 yozuv aniqlandi. Ularning turi:

| kind | Soni |
|---|---:|
| multilingual_query_pattern | 45 |
| finzanjir_specific_card | 36 |
| multilingual_knowledge_card | 30 |
| problem_model | 26 |
| founder_multilingual_mission | 10 |
| unclassified_knowledge_record | 8 |
| domain_alias | 6 |
| specific_learning_card | 5 |
| domain_learning_card | 5 |
| html_explicit_qa | 5 |
| finzanjir_multilingual_foundation | 5 |
| founder_multilingual_bio | 4 |
| multilingual_domain_alias | 2 |
| architecture_knowledge | 1 |

Bu 188 yozuvning hammasi bir xil turdagi faktik bilim emas. Ularning ichida savol yo‘naltirish patternlari, aliaslar, loyiha falsafasi, muallifga oid ma’lumotlar, modeldan hosil bo‘lgan candidate va bilim kartalari bor. Ularni bitta tekis javob korpusiga aylantirish noto‘g‘ri.

## 2. Approval va authority taqsimoti

| approval | Soni |
|---|---:|
| candidate | 134 |
| unclassified | 40 |
| author_confirmed_project_philosophy | 10 |
| author_visible_on_direct_request | 4 |

| authority | Soni |
|---|---:|
| candidate_learning | 75 |
| source_unclassified | 40 |
| source_derived_candidate | 33 |
| author_provided | 14 |
| model_generated_candidate | 10 |
| index_metadata | 8 |
| project_source_synthesis | 5 |
| source_derived_or_architecture_candidate | 3 |

Til maydonlari: und=65, uz=30, en=25, ru=23, kaa=23, kk=22. 65 ta und yozuvda tilni taxmin bilan belgilamaslik kerak; asl matn va manba orqali aniqlash talab qilinadi.

## 3. Muallifga oid ma’lumotlar va privacy

- 4 ta founder_multilingual_bio yozuvi author_visible_on_direct_request va direct_author_question_only ko‘rinishida belgilangan.
- 10 ta founder_multilingual_mission yozuvi author_confirmed_project_philosophy va author_or_project_philosophy_question doirasida belgilangan.
- Qolgan 174 yozuvda access/access_scope/visibility maydoni yo‘q. Bu avtomatik ravishda ommaga chiqarishga ruxsat bor degani emas.
- Shuning uchun yangi FINZANJIR KB’da access policy aniq bo‘lmagan yozuvlar default deny yoki restricted review holatida turishi kerak; ayniqsa muallif profili va shaxsiy kuzatuvlar ommaviy qidiruvga avtomatik berilmaydi.

## 4. ZIP-1 bilan bog‘lash

- 36 ta finzanjir_specific_card va 30 ta multilingual_knowledge_card ichidagi ta’riflar ZIP-1 V14, AI hujjatlari, 16 qatlam, signal va FDP matnlari bilan source-by-source bog‘lanishi kerak.
- 45 ta multilingual_query_pattern va alias yozuvlari bilim mazmuni emas, retrieval/routing qatlami uchun alohida saqlanadi.
- 26 ta problem_model yozuvi ehtimoliy muammo modeli sifatida qoladi; dalil va statusi tekshirilmasdan faktga ko‘tarilmaydi.
- 10 ta mission va 4 ta bio yozuvi umumiy loyiha javoblariga avtomatik qo‘shilmaydi; faqat mos savol va ruxsat doirasida ko‘rsatiladi.
- 8 ta unclassified yozuv karantinda qoladi, metadata to‘ldirilmaguncha javobda ishlatilmaydi.

## 5. Import siyosati

1. FINZANJIR domeni 188 yozuvini to‘liq “tayyor bilim” deb import qilmaslik.
2. Query pattern/alias, factual candidate, project philosophy, author-only, model-generated, problem model va architecture yozuvlarini alohida turlarga ajratish.
3. Har bir yozuvga original ID, source refs, source hash, language, content type, author attestation, independent review, approval, privacy scope va relation fields qo‘shish.
4. Bir xil ta’rif turli tillarda bo‘lsa, ularni dublikat sifatida o‘chirib yubormaslik; bitta concept ID ostida til variantlari va original record ID’lari saqlanishi kerak.
5. Manba ko‘rsatilmagan yoki source_unclassified yozuvlar faktik javobga asos bo‘lmasin.
6. Model-generated candidate yozuvlar muallif yoki ekspert tasdig‘isiz authoritative qatlamga o‘tmasin.

**Xulosa:** V317 FINZANJIR domenida foydali routing va konsept kartalari bor, ammo ularni ZIP-1 manbalariga bog‘lash, privacy va tasdiq holatini aniqlash zarur. Hozircha bu 188 yozuvning to‘liq importi ham, ekspert tasdig‘i ham bajarilgan emas.
