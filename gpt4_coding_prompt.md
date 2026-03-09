# GPT-4 Three-Theory Coding Prompt

You are an expert in educational theory and qualitative research coding. Your task is to classify a student narrative against three major theoretical frameworks.

## THEORETICAL FRAMEWORKS

### 1. CRITICAL PEDAGOGY (Freire)
Education is a political act that can reproduce or challenge inequality. Focus on how narratives reveal:
- **Student Agency**: Evidence of student voice, empowerment, or willingness to act
- **Structural Barriers**: Systemic obstacles, injustice, or inequitable conditions
- **Conscientization**: Student awareness of how social systems affect them
- **Liberation/Constraint**: Movement toward freedom or deeper constraint

**Coding Instructions**: Look for language showing consciousness of barriers, agentive responses, or expressions of empowerment/disempowerment.

---

### 2. ECOLOGICAL SYSTEMS THEORY (Bronfenbrenner)
Student experiences are shaped by nested systems influencing each other. Identify which level(s) most affect the student:
- **Microsystem**: Immediate environment (family, school, peer relationships, workplace)
- **Mesosystem**: Connections between microsystems (e.g., family-school relationships)
- **Exosystem**: Indirect influences (parents' workplace, educational policies, economic conditions)
- **Macrosystem**: Societal ideologies, values, culture, laws
- **Chronosystem**: Historical/temporal context (life transitions, major events)

**Coding Instructions**: Identify which level(s) the student emphasizes most. Most narratives will mention multiple levels—identify the 1-2 DOMINANT levels.

---

### 3. BOURDIEU'S THEORY OF CAPITAL & HABITUS
Students accumulate four forms of capital that determine educational and social outcomes:
- **Economic Capital**: Financial resources, income, material assets, employment status
- **Social Capital**: Networks, relationships, institutional connections, support systems
- **Cultural Capital**: Educational credentials, knowledge, language skills, cultural practices
- **Symbolic Capital**: Status, prestige, recognition, respect, legitimacy in society

For each capital type, classify as:
- **DEFICIT**: Student explicitly mentions lacking, struggling with, or needing this capital
- **ASSET**: Student explicitly mentions having, building, or leveraging this capital
- **ABSENT**: Capital is NOT mentioned or discussed in the narrative at all

**Coding Instructions** (Use specific language/themes as evidence, not speculation):
- **Economic deficit** (explicit): "can't afford," "need to work," "financial stress," "money problems," "struggling financially"
- **Economic asset** (explicit): "got scholarship," "parents support," "earning income," "financial stability"
- **Economic absent**: Narrative never discusses finances, money, work, or employment
- **Social deficit** (explicit): "no support," "isolated," "family problems," "no mentor," "alone," "don't have connections"
- **Social asset** (explicit): "family helped," "friends support," "mentor/professor helped," "community support"
- **Social absent**: Narrative never discusses relationships, support systems, or social networks
- **Cultural deficit** (explicit): "unprepared," "don't know," "no credentials," "behind," "underprepared"
- **Cultural asset** (explicit): "good student," "high GPA," "learning," "degree," "educated," "knowledge"
- **Cultural absent**: Narrative never discusses education, credentials, knowledge, or academic readiness
- **Symbolic deficit** (explicit): "shame," "not good enough," "imposter," "expected to fail," "invisible," "doubt"
- **Symbolic asset** (explicit): "proud," "overcame," "resilient," "recognized," "valued," "confident"
- **Symbolic absent**: Narrative never discusses status, recognition, respect, or self-perception

---

## STUDENT NARRATIVE

{NARRATIVE_TEXT}

---

## REQUIRED OUTPUT FORMAT

Return ONLY valid JSON (no markdown, no extra text) with this exact structure:

```json
{
  "critical_pedagogy": {
    "student_agency": "high" | "moderate" | "low" | "absent",
    "structural_barriers_evident": true | false,
    "consciousness_of_barriers": "high" | "moderate" | "low",
    "summary": "Brief 1-2 sentence summary of student's agency/constraint",
    "quotes": ["quote1", "quote2"]
  },
  "ecological_systems": {
    "dominant_level": "microsystem" | "mesosystem" | "exosystem" | "macrosystem" | "chronosystem",
    "secondary_level": "microsystem" | "mesosystem" | "exosystem" | "macrosystem" | "chronosystem" | null,
    "microsystem_elements": ["element1", "element2"],
    "summary": "Brief explanation of dominant system level(s)"
  },
  "bourdieu_capital": {
    "economic": "deficit" | "asset" | "absent",
    "social": "deficit" | "asset" | "absent",
    "cultural": "deficit" | "asset" | "absent",
    "symbolic": "deficit" | "asset" | "absent",
    "dominant_capital_need": "economic" | "social" | "cultural" | "symbolic",
    "dominant_capital_strength": "economic" | "social" | "cultural" | "symbolic" | null,
    "summary": "Brief summary of capital profile"
  },
  "overall_summary": "2-3 sentence synthesis: How do all three theories help us understand this student's experience?"
}
```

---

## INSTRUCTIONS FOR CODING

1. **Read the entire narrative carefully** before making classifications.
2. **Use evidence from the text** - Do NOT make assumptions or inferences beyond what is explicitly stated.
3. **For Bourdieu**: IMPORTANT - If a capital type is never mentioned or discussed, code it as "absent" rather than inferring deficit or asset. A narrative can have BOTH deficits and assets in the same capital type, OR it can omit the capital entirely.
4. **For Ecological Systems**: Most narratives will show multiple levels—pick the 1-2 that most dominate student's experience.
5. **For Critical Pedagogy**: Look for language of consciousness, agency, empowerment, or constraint.
6. **CRITICAL RULE**: Never force a classification when sufficient evidence is absent. Use "absent," "low," or "null" rather than guessing.
7. **Be specific in summaries**: Don't just repeat definitions—show what THIS student's narrative reveals using direct language from the text.

---

## VALIDITY CHECK

Before returning JSON:
- [ ] Does the JSON parse and validate?
- [ ] Have I cited evidence from the narrative?
- [ ] Am I using the student's own language/voice?
- [ ] Does the summary synthesize across theories?
