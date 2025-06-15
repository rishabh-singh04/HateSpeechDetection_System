--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: policy_documents; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.policy_documents (
    id integer NOT NULL,
    name character varying(255),
    content text
);


ALTER TABLE public.policy_documents OWNER TO admin;

--
-- Name: policy_documents_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.policy_documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.policy_documents_id_seq OWNER TO admin;

--
-- Name: policy_documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.policy_documents_id_seq OWNED BY public.policy_documents.id;


--
-- Name: query_logs; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.query_logs (
    id integer NOT NULL,
    query text,
    results_count integer,
    created_at timestamp without time zone
);


ALTER TABLE public.query_logs OWNER TO admin;

--
-- Name: query_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.query_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.query_logs_id_seq OWNER TO admin;

--
-- Name: query_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.query_logs_id_seq OWNED BY public.query_logs.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    full_name character varying(100),
    is_active boolean,
    is_superuser boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: policy_documents id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.policy_documents ALTER COLUMN id SET DEFAULT nextval('public.policy_documents_id_seq'::regclass);


--
-- Name: query_logs id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.query_logs ALTER COLUMN id SET DEFAULT nextval('public.query_logs_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: policy_documents; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.policy_documents (id, name, content) FROM stdin;
1	Google Policy	YouTube and Google Hate Speech Policy\n\nOverview\nGoogle prohibits hate speech across its platforms (YouTube, Blogger, etc.) to foster respectful and safe communities. Hate speech includes any content that promotes violence, discrimination, or hatred against individuals or groups based on protected attributes.\n\nCovered Attributes\n- Race, ethnicity, and nationality\n- Religion and caste\n- Disability or health condition\n- Age, gender identity, or sexual orientation\n- Immigration status or veteran status\n\nProhibited Content\n- Promoting superiority of one group over another\n- Justifying or denying well-documented hate events (e.g., genocide)\n- Mocking victims of discrimination or violence\n- Content that incites violence or segregation\n- Coded language or ΓÇ£dog whistlesΓÇ¥ used to evade detection\n\nEnforcement Criteria\nContent is reviewed based on context, tone, intent, and metadata. Hate speech disguised as comedy, education, or news will still be removed if it promotes harm.\n\nGraduated Penalty System\n- First Strike: Video removed, channel warning\n- Second Strike: 1-week posting restriction\n- Third Strike: Channel termination\n- Severe single violations: Immediate channel ban\n\nUser Reporting & AI Detection\nGoogle uses a mix of AI classifiers, human moderators, and community flagging to detect hate speech. All flagged content is reviewed by trained reviewers within 24 hours.\n\nAppeals Process\nUsers can appeal strikes through YouTube Studio. Successful appeals restore removed content and lift any active restrictions.\n\nPolicy Development\nGoogle updates policies quarterly based on partner NGO recommendations, UN guidelines, and evolving hate trends (e.g., AI-generated hate content).\n\n
2	Indian Penal Code	Indian Penal Code Provisions on Hate Speech\n\nOverview\nIndia addresses hate speech through various sections of the Indian Penal Code (IPC) and related legal provisions to maintain public order, prevent communal disharmony, and protect citizens' dignity.\n\nRelevant Sections\n- **Section 153A**: Promoting enmity between different groups on grounds of religion, race, language, or caste. Punishable with up to 3 years imprisonment and/or fine.\n- **Section 295A**: Deliberate and malicious acts intended to outrage religious feelings. Punishable with up to 3 years imprisonment and/or fine.\n- **Section 505(1)**: Publishing or circulating statements with intent to incite hatred or alarm among the public. Covers rumor-mongering that leads to fear or violence.\n- **IT Act Section 66A** (struck down but relevant historically): Criminalized offensive electronic communication.\n\nDefinition of Hate Speech\nThere is no single definition, but courts recognize hate speech as any expression that promotes hatred against a protected group and could disturb public peace.\n\nJudicial Principles\n- Intent, tone, and impact matter more than literal words.\n- Truth is not always a defense if the speech is inflammatory.\n- Satire or parody is not protected if it incites harm.\n\nEnforcement\n- FIR can be registered based on complaint.\n- Courts can order take-downs or injunctions.\n- Police may issue preventive notices under CrPC.\n\nExamples of Punishable Acts\n- Making inflammatory speeches during election campaigns\n- Posting communal memes or misinformation\n- Threats based on caste or religion\n\nPolicy Notes\nThe Supreme Court has emphasized restraint in using these laws and the need to protect free speech unless there's real incitement to violence.\n
3	Meta Policy	Meta Community Standards: Hate Speech and Harmful Content\n\nOverview\nMeta prohibits hate speech, defined as a direct attack against people on the basis of protected characteristics: race, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity, and serious disease.\n\nDefinitions\n- Direct attacks include violent or dehumanizing speech, harmful stereotypes, statements of inferiority, expressions of contempt, disgust or dismissal, cursing, and calls for exclusion or segregation.\n- Tier 1 violations include dehumanizing comparisons, mocking victims of hate crimes, and advocating for violence.\n- Tier 2 violations include generalizations about inferiority and statements of contempt.\n- Tier 3 violations include exclusionary statements and calls for segregation.\n\nExceptions\nWe allow content discussing hate speech for educational or awareness purposes. Satire and humor related to hate speech may be allowed if it doesn't reinforce stereotypes or directly attack protected groups.\n\nContent Removal Guidelines\n- Content that explicitly advocates for violence based on protected characteristics will be removed immediately.\n- Dehumanizing comparisons between protected groups and animals, insects, pests, disease, or criminals will be removed.\n- Claims that protected groups are inherently inferior, deficient, or undesirable will be removed.\n\nEnforcement Actions\n- First violation: Warning and content removal\n- Second violation: Temporary restriction (24 hours)\n- Third violation: Temporary restriction (3-7 days)\n- Repeated violations: Account review which may lead to permanent suspension\n- Severe violations: Immediate and permanent account suspension\n\nAppeals Process\nUsers can appeal content decisions through the Help Center. Appeals are typically reviewed within 24-48 hours by a separate reviewer.\n\nPolicy Updates\nThese policies are regularly reviewed and updated based on expert guidance, industry standards, and community feedback. Users are notified of significant policy changes via the Meta Newsroom.\n
4	Reddit Policy	Reddit Content Policy: Hate Speech and Abusive Behavior\n\nOverview\nReddit is a platform for open discussion, but we prohibit content that promotes hate based on identity or vulnerability. Hate speech includes attacks, slurs, and negative generalizations targeting groups based on race, ethnicity, religion, gender identity, sexual orientation, disability, or immigration status.\n\nDefinitions\n- Hate speech includes calls for violence, use of racial or homophobic slurs, dehumanizing metaphors, and content that promotes prejudice or exclusion.\n- Content that glorifies historical atrocities (e.g., Holocaust denial) or justifies discrimination is explicitly prohibited.\n- Systematic harassment and ΓÇ£brigadingΓÇ¥ (targeted attacks by groups) against marginalized communities are also considered hate.\n\nProtected Characteristics\nWe do not allow attacks based on:\n- Race or ethnicity\n- Religion or caste\n- National origin\n- Gender identity or presentation\n- Sexual orientation\n- Serious medical conditions or disabilities\n- Socioeconomic status (in the context of hate)\n\nContent Moderation Guidelines\n- Posts using slurs or expressing hatred toward a protected group will be removed.\n- Subreddits dedicated to hateful ideologies will be banned.\n- Harassment, even if veiled in sarcasm or satire, will be treated as a policy violation.\n\nEnforcement Actions\n- First violation: Content removed, warning issued.\n- Second violation: Temporary account ban (3 days).\n- Repeated violations: Subreddit-specific or global account ban.\n- Hate-based communities: Immediate subreddit quarantine or ban.\n\nAppeals Process\nUsers can appeal bans by contacting Reddit admins through the appeals portal. Moderator bans can be appealed within the specific subreddit, but platform-level bans must go through RedditΓÇÖs admin team.\n\nTransparency and Policy Revisions\nReddit publishes an annual Transparency Report on enforcement of hate speech policies and moderates with community feedback to refine guidelines.\n
5	Us Laws	U.S. Federal & Constitutional Position on Hate Speech\n\nOverview\nThe First Amendment of the U.S. Constitution protects freedom of speech, but there are exceptions for incitement, threats, and obscenity. Hate speech is not a distinct legal category in U.S. law, but some forms can still be prosecuted under specific circumstances.\n\nProtected vs. Unprotected Speech\n- **Protected**: Offensive opinions, political rhetoric, satire, even hate speech unless it crosses legal thresholds.\n- **Unprotected**: Incitement to imminent lawless action (Brandenburg v. Ohio), true threats, harassment, and speech that incites violence.\n\nApplicable Federal Laws\n- **18 U.S.C. ┬º 245**: Criminalizes interfering with federally protected activities (voting, education) based on race, color, religion, or national origin.\n- **Matthew Shepard & James Byrd, Jr. Hate Crimes Prevention Act (2009)**: Expands hate crime definition to include gender identity and sexual orientation.\n- **Civil Rights Act (Title VI and VII)**: Allows prosecution for workplace or institutional discrimination linked to hate speech.\n\nUniversity & Online Policies\n- Most hate speech enforcement in the U.S. occurs through:\n  - Campus conduct codes\n  - Platform-specific community guidelines\n  - Workplace anti-harassment policies\n\nSupreme Court Guidance\n- Mere offense is not a justification for suppression (Matal v. Tam, 2017).\n- Speech must pose a "true threat" or incite imminent violence to be criminalized.\n\nEnforcement Bodies\n- DOJ Civil Rights Division\n- FBI (hate crimes investigations)\n- EEOC (workplace harassment cases)\n\nPolicy Note\nWhile hate speech may not be banned, it can lead to social media bans, civil suits, loss of employment, or public backlash.\n
\.


--
-- Data for Name: query_logs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.query_logs (id, query, results_count, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, username, email, hashed_password, full_name, is_active, is_superuser, created_at, updated_at) FROM stdin;
1	admin	admin@example.com	$2b$12$IczCStUJiXqlix8IuE.6fefNILh7WxlnWt8kSl.UnrTX80BvvEkEq	Admin User	t	t	2025-06-10 03:28:57.767581+05:30	\N
2	moderator	moderator@example.com	$2b$12$xKe3pj8/jO8YQmjpU0TLaeFGMqUsxF9EVHhgLoYGJrs8uX1.1bToG	Moderator User	t	f	2025-06-10 03:28:57.773013+05:30	\N
3	user2	user2@example.com	$2b$12$hIBJjQIAcIy0OFLv6IhA5OnigJ2754VY4vEeA3vCnAa4.0D0BsQa2	User2	t	f	2025-06-10 12:35:16.564794+05:30	\N
4	user1	user1@example.com	$2b$12$eIjc43pmbIkkseOYWzKYweDFtkRIXo7QmzOjtuY03i0lGifuA4N36	user1	t	f	2025-06-11 09:21:36.109958+05:30	\N
5	user3	user3@gmail.com	$2b$12$HqVsrFkyRJkdQVWekFzIIeh8RHLxHxpbM48p1HrKwonAA./T3WRVG	User3	t	f	2025-06-11 11:58:22.160301+05:30	\N
\.


--
-- Name: policy_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.policy_documents_id_seq', 5, true);


--
-- Name: query_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.query_logs_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: policy_documents policy_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.policy_documents
    ADD CONSTRAINT policy_documents_pkey PRIMARY KEY (id);


--
-- Name: query_logs query_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.query_logs
    ADD CONSTRAINT query_logs_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- PostgreSQL database dump complete
--

