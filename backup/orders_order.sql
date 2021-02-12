--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: orders_order; Type: TABLE; Schema: public; Owner: emre
--

CREATE TABLE public.orders_order (
    id integer NOT NULL,
    recipient character varying(50) NOT NULL,
    shipping_label character varying(100),
    total numeric(10,2),
    discount numeric(10,2),
    shipping_fee numeric(10,2),
    profit numeric(10,2),
    paid boolean NOT NULL,
    fulfillment boolean NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    ordered_by_id integer NOT NULL,
    stripe_id character varying(150) NOT NULL,
    coupon_id integer,
    note character varying(1000),
    attachment character varying(100)
);


ALTER TABLE public.orders_order OWNER TO emre;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: emre
--

CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_order_id_seq OWNER TO emre;

--
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: emre
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders_order.id;


--
-- Name: orders_order id; Type: DEFAULT; Schema: public; Owner: emre
--

ALTER TABLE ONLY public.orders_order ALTER COLUMN id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- Data for Name: orders_order; Type: TABLE DATA; Schema: public; Owner: emre
--

COPY public.orders_order (id, recipient, shipping_label, total, discount, shipping_fee, profit, paid, fulfillment, created, updated, ordered_by_id, stripe_id, coupon_id, note, attachment) FROM stdin;
82	Marilyse Hamelin	uploads/Marilyse_Hamelin_LABEL.pdf	11.90	0.00	\N	\N	t	t	2021-01-22 00:51:04.952311+00	2021-02-02 23:22:53.000184+00	19	ch_1ICDs1LDH0j3JuXLcMcJXtlD	\N	\N	
43	Brian Payne	uploads/Brian_Payne_LABEL.pdf	11.90	0.00	\N	\N	f	t	2021-01-09 21:32:09.734407+00	2021-01-13 20:34:24.170098+00	19		\N	On the “I” please do not include a top or bottom horizontal line. Just a straight vertical line	\N
62	LE BAUT Victoria	uploads/LE_BAUT_Victoria_LABEL.pdf	94.25	0.00	\N	\N	t	t	2021-01-18 21:17:01.009929+00	2021-01-20 20:35:24.721929+00	19	ch_1IB56JLDH0j3JuXLkm9yGGRh	\N	\N	\N
60	Susan Edlitz	uploads/Susan_Edlitz_LABEL_c2gJh8P.pdf	7.25	0.00	\N	\N	t	t	2021-01-18 20:29:28.233173+00	2021-01-20 20:35:34.000034+00	19	ch_1IB4NILDH0j3JuXLvYSgk5XR	\N	\N	\N
47	toni		285.76	0.00	\N	\N	f	t	2021-01-11 18:44:03.090643+00	2021-01-18 19:03:11.740338+00	22		\N	\N	\N
119	Barbara Seagrass	uploads/Barbara_Seagrass.pdf	7.25	0.00	\N	\N	t	t	2021-01-26 12:00:03.768362+00	2021-02-01 17:54:24.766841+00	19	ch_1IDqDULDH0j3JuXLD885MbQx	\N	Font 8/Smokey grey/SGS	
32	Rebeca roberts	uploads/Rebecca_Roberts_labels.pdf	7.90	0.00	\N	\N	t	t	2021-01-08 21:00:52.134911+00	2021-01-09 00:09:18.626118+00	19	ch_1I7S4xLDH0j3JuXLBXZRKTJe	\N	\N	\N
56	Esmira Sadulleyeva	uploads/labels-esmira_sadullayeva.pdf	7.25	0.00	\N	\N	t	t	2021-01-15 17:13:15.690258+00	2021-01-18 20:00:47.899914+00	25	ch_1I9vsCLDH0j3JuXLUbKmBYN7	\N	\N	\N
10	Judith Russell	uploads/30.12.2020_label.pdf	9.70	0.00	\N	\N	t	t	2020-12-30 18:48:37.323786+00	2021-01-04 20:46:19.840583+00	14	ch_1I49qMLDH0j3JuXLQ8A4BK12	\N	\N	\N
81	Christine	uploads/Christine_LABEL.pdf	7.25	0.00	\N	\N	t	t	2021-01-22 00:46:34.043342+00	2021-01-26 21:18:45.420626+00	19	ch_1ICDnULDH0j3JuXLxkhgPZVm	\N	Gift message:\r\nHappy Valentine’s Day and I hope your podcast takes off as you envision it to !\r\n...MARKED AS GİFT...\r\n\r\nFront Text Only\r\nI Gotta Hear This using font Bangers( font 1 ) gösteriyor.	\N
11	Maryln Adams	uploads/labels-864f2535bfdc1c7079cd05d1d06dd30e.pdf	237.00	0.00	\N	\N	t	t	2021-01-04 19:32:51.596482+00	2021-01-06 18:25:30.417643+00	13	ch_1I5yonLDH0j3JuXLDgC5CTk3	\N	\N	\N
95	Sarah Wanshura	uploads/Sarah_Wanshura_LABEL.pdf	7.25	0.00	\N	\N	t	t	2021-01-22 19:35:36.196142+00	2021-01-26 21:20:57.852617+00	19	ch_1ICVQfLDH0j3JuXLfyE0NQK5	\N	\N	\N
58	Toni		89.95	0.00	\N	\N	f	t	2021-01-18 19:24:28.56611+00	2021-02-02 23:24:23.042541+00	22		\N	\N	
13	Brian Derochie	uploads/labels-f4ffd301daf05c34078846d890ecc487.pdf	9.90	0.00	\N	\N	t	t	2021-01-06 18:23:58.468769+00	2021-01-07 21:53:29.104633+00	13	ch_1I6gghLDH0j3JuXLWFkpG0PH	\N	\N	\N
12	Halley Ramsey	uploads/labels-feaa5f8b7dea73291782fa46a627ba68.pdf	7.90	0.00	\N	\N	t	t	2021-01-05 17:17:41.664347+00	2021-01-07 21:53:37.369018+00	13	ch_1I6JBkLDH0j3JuXLHppsqoPb	\N	\N	\N
136	Mandy Chislock	uploads/Mandy_Chislock.pdf	7.25	0.00	\N	\N	t	t	2021-01-30 13:30:35.847941+00	2021-02-02 22:29:02.961441+00	19	ch_1IFJXGLDH0j3JuXLGgPWZ13L	\N	Front Text Only\r\nFont 1/ White thread/ My wife is hot & My dog is cute	
83	Eryne Caprara	uploads/Eryne_Caprara_LABEL.pdf	9.99	0.00	\N	\N	t	t	2021-01-22 00:58:33.382481+00	2021-01-27 19:29:02.746076+00	19	ch_1ICDz5LDH0j3JuXLcsjCiw2X	\N	Size: Unisex - XS\r\nColor: White	\N
97	kayla maness	uploads/kayla_maness_LABEL.pdf	7.25	0.00	\N	\N	t	t	2021-01-22 19:47:54.081387+00	2021-01-27 18:41:31.943534+00	19	ch_1ICVc0LDH0j3JuXLuiLuRJuM	\N	\N	\N
57	Shannon M Petyan	uploads/labels-17.01.2021.pdf	14.50	0.00	\N	\N	t	t	2021-01-17 11:11:56.706589+00	2021-01-19 22:02:25.057407+00	14	ch_1IAZByLDH0j3JuXLCk8EM1ts	\N	font  : 13 blac beanie 2 adet1. Smokey grey KENZY 2.Smokey greyNATE	\N
61	Myranda Pauley	uploads/Myranda_Pauley.pdf	7.25	0.00	\N	\N	t	t	2021-01-18 20:45:19.085143+00	2021-01-20 20:35:50.401664+00	19	ch_1IB4bOLDH0j3JuXLP5lvzYZf	\N	\N	\N
63	Jenna Schumann	uploads/Jenna_Schumann.pdf	7.25	0.00	\N	\N	t	t	2021-01-18 21:21:29.414582+00	2021-01-20 20:36:03.265133+00	19	ch_1IB5AaLDH0j3JuXLoCttQbvQ	\N	\N	\N
28	Tionna Gordon	uploads/Tionna_Gordon_labels_LtH6Gy2.pdf	23.70	0.00	\N	\N	t	t	2021-01-08 18:34:24.302423+00	2021-01-08 22:06:51.900648+00	19	ch_1I7PnwLDH0j3JuXLa1O8nRTV	\N	\N	\N
64	Helen Harrnacker	uploads/Helen_Harrnacker_LABEL.pdf	7.25	0.00	\N	\N	t	t	2021-01-19 09:06:24.246605+00	2021-01-20 20:36:12.655887+00	19	ch_1IBGAbLDH0j3JuXLV8oo4U2L	\N	\N	\N
31	Valanchie21@gmail.com	uploads/Valanchie21gmail.com__labels.pdf	7.90	0.00	\N	\N	t	t	2021-01-08 20:48:28.261668+00	2021-01-08 22:14:52.314685+00	19	ch_1I7RvZLDH0j3JuXLDzFakovh	\N	\N	\N
30	Leslie Villa	uploads/Leslie_Villa_labels_5d8KY5T.pdf	7.90	0.00	\N	\N	t	t	2021-01-08 19:30:28.111484+00	2021-01-08 22:15:04.148471+00	19	ch_1I7Qi8LDH0j3JuXLAI16aiGi	\N	\N	\N
65	Mackenzie Kowalczyk	uploads/Mackenzie_Kowalczyk_LABEL.pdf	7.25	0.00	\N	\N	t	t	2021-01-19 09:21:12.535493+00	2021-01-20 20:36:23.360893+00	19	ch_1IBGOvLDH0j3JuXL7UnlvMax	\N	\N	\N
66	Neha Santhebennur	uploads/Neha_Santhebennur_LABEL.pdf	7.25	0.00	\N	\N	t	t	2021-01-19 10:04:17.736005+00	2021-01-20 20:36:29.660047+00	19	ch_1IBH4YLDH0j3JuXLzLxAW6LR	\N	\N	\N
78	Noelani Garcia	uploads/Noelani_Garcia_LABEL_3NQHY9R.pdf	7.25	0.00	\N	\N	t	t	2021-01-22 00:28:09.205151+00	2021-01-26 21:18:05.74398+00	19	ch_1ICDWELDH0j3JuXLsWS2aYkA	\N	\N	\N
80	Brian Kraljic	uploads/Brian_Kraljic_LABEL_PbGCihZ.pdf	7.25	0.00	\N	\N	t	t	2021-01-22 00:37:51.859208+00	2021-01-26 21:18:31.282884+00	19	ch_1ICDf2LDH0j3JuXLaTsUly7h	\N	FONT VE İPLİK BELİRTMEMİŞ.	\N
39	Susan Edlitz	uploads/Susan_Edlitz_LABEL.pdf	31.60	0.00	\N	\N	t	t	2021-01-09 21:06:36.360478+00	2021-01-12 00:14:56.379999+00	19	ch_1I7oe2LDH0j3JuXLOR5zCZ5X	\N	\N	\N
40	Dawn French	uploads/Dawn_French_LABEL.pdf	7.90	0.00	\N	\N	t	t	2021-01-09 21:10:18.377098+00	2021-01-12 00:15:08.222912+00	19	ch_1I7ohcLDH0j3JuXL3hv77gDQ	\N	\N	\N
42	Amanda Raniolo	uploads/Amanda_Raniolo_LABEL.pdf	7.90	0.00	\N	\N	t	t	2021-01-09 21:26:20.097885+00	2021-01-12 00:15:17.047212+00	19	ch_1I7ox7LDH0j3JuXLzVWTMduh	\N	Marked as giftGift message included  :  Merry Christmas in February ya crackhead <3	\N
41	bianca garcia	uploads/bianca_garcia_LABEL.pdf	23.70	0.00	\N	\N	t	t	2021-01-09 21:18:57.485781+00	2021-01-12 00:15:28.374826+00	19	ch_1I7oq1LDH0j3JuXL3LkqcKUu	\N	\N	\N
44	Tania Barrera	uploads/Tania_Barrera_LABEL.pdf	7.90	0.00	\N	\N	t	t	2021-01-10 23:56:25.671318+00	2021-01-12 00:16:01.217967+00	19	ch_1I8DlvLDH0j3JuXLFtig45Ak	\N	\N	\N
96	Marly FireMoon	uploads/Marly_FireMoon_LABEL.pdf	7.25	0.00	\N	\N	t	t	2021-01-22 19:40:58.750248+00	2021-01-26 21:59:59.486657+00	19	ch_1ICVVILDH0j3JuXLZKYjv2za	\N	\N	\N
68	Terrica Montgomery	uploads/Terrica_Montgomery_LABEL.pdf	11.99	0.00	\N	\N	t	t	2021-01-19 19:27:32.415399+00	2021-01-26 22:07:27.653837+00	19	ch_1IBPreLDH0j3JuXLaI1lNfXi	\N	Unisex - S \r\nTasarımda kalpler kırmızı ama hesapta olan kalpler beyaz gösteriyor kırmızı tişörtün üstünde.	\N
109	debra *long	uploads/debra_label.pdf	21.75	0.00	\N	\N	t	t	2021-01-23 21:32:37.750863+00	2021-01-27 18:41:39.136576+00	19	ch_1ICtiuLDH0j3JuXLChSyKXe9	\N	Front text only /deep purple / font10	\N
110	Spencer Thomas	uploads/Spencer_Thomas_label.pdf	7.25	0.00	\N	\N	t	t	2021-01-23 21:43:22.873596+00	2021-01-27 18:41:48.063848+00	19	ch_1ICttKLDH0j3JuXLIwIDly0w	\N	Font 14/White Thread/FrontText Only	\N
111	Aisha Link	uploads/Aisha_Link_LABEL.pdf	14.50	0.00	\N	\N	t	t	2021-01-24 22:35:06.902406+00	2021-01-27 18:42:06.957045+00	19	ch_1IDHAvLDH0j3JuXLCd8ceQ6k	\N	Front Text Only\r\nFont 11/ Burnt Orange Thread/$wAgLiFe\r\n\r\nFront Text Only\r\nFont 22/Gold Thread/Poetic Ju$tice	\N
117	Lara Frenz	uploads/Lara_Frenz.pdf	7.25	0.00	\N	\N	t	t	2021-01-26 11:10:29.248356+00	2021-01-27 18:42:15.008294+00	19	ch_1IDpRaLDH0j3JuXLXxwWnepO	\N	font 14 \r\nwhite thread \r\nfront text only	\N
67	Brenda Hogue	uploads/Brenda_Hogue_LABEL.pdf	11.99	0.00	\N	\N	t	t	2021-01-19 19:21:50.68157+00	2021-01-27 19:11:09.193673+00	19	ch_1IBPm8LDH0j3JuXLkdQlR46G	\N	Unisex - M	\N
118	nicole c perugini	uploads/nicole_c_perugini.pdf	21.75	0.00	\N	\N	t	t	2021-01-26 11:26:19.67423+00	2021-01-27 18:42:30.405907+00	19	ch_1IDpglLDH0j3JuXLwAXo6NPP	\N	FONT 1 / FIFTY\r\nFONT 3 / FEROCE/ İTALİCS\r\nWHİTE THREAD\r\nBEANIE COLOR: DARK GREY	\N
70	KACIE SAMPSON	uploads/kacıe_sampson_LABEL.pdf	29.00	0.00	\N	\N	t	t	2021-01-22 00:13:48.276674+00	2021-01-26 21:17:50.447389+00	19	ch_1ICDHnLDH0j3JuXLBa8cHOCM	\N	\N	\N
124	Johnnie R Montecino	uploads/Johnnie_R_Montecino.pdf	14.50	0.00	\N	\N	t	t	2021-01-26 16:33:10.631507+00	2021-02-01 17:55:12.286146+00	19	ch_1IDuTqLDH0j3JuXLAYTOi5Wi	\N	Front Text Only\r\nbeanıe color: black\r\nfont 12\r\nwhite thread \r\nUniversity of Redlands Public Safety	
125	Deborah Zachary	uploads/Deborah_Zachary.pdf	7.25	0.00	\N	\N	t	t	2021-01-27 15:26:25.967347+00	2021-02-01 17:55:33.845004+00	19	ch_1IEG12LDH0j3JuXLiCteOSFS	\N	font ve iplik rengi belli etmemiş	
128	Cassidy Spencer	uploads/Cassidy_Spencer.pdf	29.00	0.00	\N	\N	t	t	2021-01-27 16:00:59.555146+00	2021-02-01 17:55:57.029608+00	19	ch_1IEGS7LDH0j3JuXLTMjvr1RM	\N	Front Text Only\r\n1.Font 12- graduate\r\n2.Thread- fire red\r\n3. The Miscreants	
129	Melissa Dixon	uploads/melıssa_dıxon_label.pdf	11.90	0.00	\N	\N	f	t	2021-01-27 16:34:13.74121+00	2021-02-01 17:56:09.00579+00	27		\N	Front Design Only\r\nFont 16/White thread/ INDI	
132	Salma Fariz	uploads/label_1931379684.pdf	9.99	0.00	\N	\N	t	t	2021-01-28 10:26:21.445647+00	2021-02-01 19:48:19.784388+00	20	ch_1IEaYVLDH0j3JuXLHzehPxTO	\N	\N	
126	Jana Rozada	uploads/Jana_Rozada.pdf	7.25	0.00	\N	\N	t	t	2021-01-27 15:37:52.557348+00	2021-02-01 17:55:42.61579+00	19	ch_1IEG5kLDH0j3JuXLiUNigOed	\N	Front Text Only\r\nI like Font 2/white Thread/ Wanker	
121	Brenda Hogue	uploads/Brenda_Hogue.pdf	9.99	0.00	\N	\N	t	t	2021-01-26 12:18:44.323833+00	2021-01-27 19:12:55.286051+00	19	ch_1IDqViLDH0j3JuXLORcYA8rs	\N	TASARIMDAKİ KALPLER BEYAZ OLUCAK AMA BENDE KIRMIZI VAR HESAPTA KIRMIZI TİŞÖRTÜN ÜSTÜNDE BEYAZ KALP VAR	\N
131	Julie Schoenrock	uploads/Julie_Schoenrock.pdf	7.25	0.00	\N	\N	t	t	2021-01-27 22:00:45.373816+00	2021-02-02 21:13:24.862593+00	19	ch_1IEM4cLDH0j3JuXLiJjHekn5	\N	Front Text Only\r\nFont 16/Fire Red/ (heart shape) JULIE	
141	Garrett Marshall	uploads/Garrett_Marshall.pdf	7.25	0.00	\N	\N	t	t	2021-01-30 14:30:21.396648+00	2021-02-02 21:20:37.22608+00	19	ch_1IFKT4LDH0j3JuXLqtao6WKa	\N	\N	
171	Hailee Fint	uploads/Hailee_Fint.pdf	7.25	0.00	\N	\N	t	t	2021-02-01 10:57:08.201116+00	2021-02-02 22:30:31.555774+00	19	ch_1IG06ELDH0j3JuXLkDqkQzRD	\N	Front14/white/DeadShotZay-note no spaces.	uploads/Hailee_Fint_MARKET_AS_GİFT.pdf
164	Victoria Fuerst	uploads/victoria_fuerst_Q3C806F.pdf	7.25	0.00	\N	\N	t	t	2021-01-31 19:49:12.316159+00	2021-02-02 21:21:16.810575+00	19	ch_1IFlvmLDH0j3JuXLRJCQ1Gev	\N	1. Font 14\r\n2. White thread\r\n3. VICTORDUDE	uploads/victoria_gift_message_f4uOWhL.pdf
140	Katelynn mcnicholas	uploads/Katelynn_mcnicholas_Cy9NqXC.pdf	7.25	0.00	\N	\N	t	t	2021-01-30 14:11:36.44698+00	2021-02-02 22:31:09.666713+00	19	ch_1IFKAvLDH0j3JuXLAQYPdoFg	\N	\N	
145	Jackie Gordon	uploads/Jackie_Gordon.pdf	7.25	0.00	\N	\N	t	t	2021-01-30 21:17:35.749783+00	2021-02-02 21:20:48.024605+00	19	ch_1IFQpCLDH0j3JuXLjhNNmpxP	\N	\N	
166	Angela Burton	uploads/Angela_Burton.pdf	7.25	0.00	\N	\N	t	t	2021-01-31 20:44:19.801138+00	2021-02-02 21:21:36.124435+00	19	ch_1IFmmXLDH0j3JuXLrWSXfh9P	\N	Font 2. black thread. Ken’s Lucky Fishin’ Hat	
133	Liz Burke	uploads/Liz_Burke.pdf	7.25	0.00	\N	\N	t	t	2021-01-28 13:12:57.072652+00	2021-02-02 22:28:55.136403+00	19	ch_1IEaJ4LDH0j3JuXLLSxHU0j6	\N	Front Text Only\r\nFont 6/White thread/ “I’m just rawdogging reality”	
192	Kim Zahner	uploads/label_1945804591.pdf	9.99	0.00	\N	\N	f	f	2021-02-04 16:06:41.239279+00	2021-02-04 16:06:41.239303+00	20		\N	\N	
170	Casondra Zambrano	uploads/Casondra_Zambrano.pdf	7.25	0.00	\N	\N	t	t	2021-02-01 10:53:04.662356+00	2021-02-02 22:30:23.327321+00	19	ch_1IG01tLDH0j3JuXLmBhvnBQw	\N	Font 12\r\nThread Hot Pink\r\nUpper case KILLER	
165	Erica Johns	uploads/Erica_Johns.pdf	7.25	0.00	\N	\N	t	f	2021-01-31 20:05:09.869035+00	2021-01-31 20:05:19.799755+00	19	ch_1IFmAbLDH0j3JuXLl57D5LUU	\N	font ve yazı tipi belli etmedi	uploads/victoria_gift_message_fiHiZR5.pdf
177	WIlliam Folzenlogen	uploads/WIlliam_Folzenlogen.pdf	7.25	0.00	\N	\N	t	t	2021-02-02 18:26:24.171922+00	2021-02-02 22:30:49.394341+00	19	ch_1IGTaDLDH0j3JuXLD6FEX9Xk	\N	\N	
168	Harley Garcia	uploads/Harley_Garcia.pdf	9.99	0.00	\N	\N	t	f	2021-02-01 10:22:25.454307+00	2021-02-01 10:22:53.460782+00	19	ch_1IFzYVLDH0j3JuXLtavMtqV1	\N	\N	
169	Lotte Eadler	uploads/Lotte_Eadler.pdf	9.99	0.00	\N	\N	t	f	2021-02-01 10:27:44.343119+00	2021-02-01 10:28:01.058935+00	19	ch_1IFzdTLDH0j3JuXL9h8DtkN4	\N	KALPLER BEYAZ GÖSTERİYOR ETSYDE	
180	Sheila Abrahamsson	uploads/Sheila_Abrahamsson_Fvw7beS.pdf	14.50	0.00	\N	\N	t	t	2021-02-02 19:26:44.333932+00	2021-02-02 22:59:39.134033+00	19	ch_1IGUWXLDH0j3JuXLNYIxgAXa	\N	\N	
137	Sohaib Bouaiss	uploads/Sohaib_Bouaiss.pdf	7.25	0.00	\N	\N	t	t	2021-01-30 13:55:47.648191+00	2021-02-02 23:00:19.418987+00	19	ch_1IFJvlLDH0j3JuXLYikKmpKC	\N	Front Text Only\r\n1.) Font 22\r\n2.) White letters with red heart\r\n3.) I ❤️ MY MOM	
172	Feven	uploads/labels-c321b466aa84c0e133818c0d18704915-2.pdf	79.96	0.00	\N	\N	t	f	2021-02-01 11:05:14.264692+00	2021-02-01 12:38:57.711461+00	20	ch_1IG0DhLDH0j3JuXL2Wkl6p6j	\N	Please center the image to the sweatshirt (vertically not horizontally). This order has marked as gift. Thank you.	
127	Patricia Hansen	uploads/Patricia_Hansen.pdf	7.25	0.00	\N	\N	t	t	2021-01-27 15:47:40.387321+00	2021-02-01 17:55:49.811812+00	19	ch_1IEGHQLDH0j3JuXLEiBMRAbW	\N	Front Text Only\r\nFont 12/neon Orange thread/Liammowlawn	
120	Erica Thornton	uploads/Erica_Thornton.pdf	7.25	0.00	\N	\N	t	t	2021-01-26 12:03:07.511251+00	2021-02-01 17:54:35.011315+00	19	ch_1IDqGOLDH0j3JuXLqlikKjEY	\N	Font 8/ White Thread/ 2nd Favorite	
122	Lara Hirschowitz	uploads/Lara_Hirschowitz.pdf	50.75	0.00	\N	\N	t	t	2021-01-26 12:25:15.275194+00	2021-02-01 17:54:43.952513+00	19	ch_1IDqboLDH0j3JuXL7RP15gzo	\N	Font 14\r\nWhite thread\r\nBeanie Color: Dark Grey\r\n2021 #50	
123	Shernice Lazare	uploads/Shernice_Lazare.pdf	23.25	0.00	\N	\N	t	t	2021-01-26 13:37:12.997211+00	2021-02-01 17:54:58.187881+00	19	ch_1IDrjVLDH0j3JuXLFGgWkhR1	\N	1. FRONT: JUST DID IT! (Burnt Orange) Font 20\r\nBACK: MISHA (Burnt Orange) Font 23\r\n\r\n2. FRONT: JUST DID IT! (Burnt Orange) Font 20\r\nBACK: JOE (Burnt Orange) Font 23\r\n\r\n3. FRONT: JUST DID IT! (Burnt Orange) Font 20\r\nBACK: SLOAN (Burnt Orange) Font 23	
167	Mirline Valery	uploads/Mirline_Valery.pdf	7.75	0.00	\N	\N	t	t	2021-01-31 21:42:26.467939+00	2021-02-02 23:23:51.079213+00	19	ch_1IFngmLDH0j3JuXLyUfOQrl8	\N	\N	
130	Toi Timpke	uploads/Toi_Timpke.pdf	7.25	0.00	\N	\N	t	t	2021-01-27 21:54:44.534204+00	2021-02-02 21:13:15.143917+00	19	ch_1IELyjLDH0j3JuXLtrOVB8gJ	\N	Front Text Only\r\nFont 23/white thread/Papi Chulo	
144	John	uploads/John.pdf	7.25	0.00	\N	\N	t	t	2021-01-30 21:14:42.155621+00	2021-02-02 21:20:23.713375+00	19	ch_1IFQmMLDH0j3JuXLnpK7dCy0	\N	normal yazı tipi dedi	
150	John Nugent	uploads/john_nugent.pdf	7.25	0.00	\N	\N	t	t	2021-01-31 13:38:33.881089+00	2021-02-02 21:20:59.7914+00	19	ch_1IFg8TLDH0j3JuXLppuK43L3	\N	Font Type: 19 Permanent Marker\r\nThread Color: Yellow Bird\r\nText: Get Dead	
181	Kieran	uploads/Kieran.pdf	14.50	0.00	\N	\N	t	f	2021-02-03 00:46:27.86186+00	2021-02-03 00:46:38.848812+00	19	ch_1IGZVxLDH0j3JuXLITelgWS0	\N	font iplik belli etmedi	
182	Pamela Rux	uploads/Pamela_Rux.pdf	7.25	0.00	\N	\N	t	f	2021-02-03 00:48:44.792392+00	2021-02-03 00:49:04.299475+00	19	ch_1IGZYILDH0j3JuXLGvSVo45A	\N	font iplik belli değil	
185	Margaret Bradbury	uploads/Margaret_Bradbury_label.pdf	7.25	0.00	\N	\N	t	f	2021-02-03 00:56:57.767932+00	2021-02-03 00:57:19.063096+00	19	ch_1IGZgHLDH0j3JuXLy1FuPEbS	\N	yazı tipi ve iplik rengi belirtmedi	uploads/Margaret_Bradbury_bWM17Bx.pdf
143	Jenny Posey	uploads/labels-befcb9233c0fdea6e35b0711970c822a_1zZ4sIR.pdf	9.25	0.00	\N	\N	t	t	2021-01-30 19:12:59.629946+00	2021-02-03 18:53:51.476176+00	20	ch_1IFOtcLDH0j3JuXLJYItDHhs	\N	\N	
162	Sasha Nieves	uploads/labels-461037f8ecd37b0b0ce6000125fd11d8_cGoGFS9.pdf	11.99	0.00	\N	\N	t	t	2021-01-31 15:50:58.869261+00	2021-02-03 23:15:09.081167+00	20	ch_1IFiDILDH0j3JuXLV7fFQPbO	\N	This order has marked as gift and a gift note specified in the attachment.	uploads/download-2021-01-31_8XI7Cfr.pdf
195	Kourtney beasley	uploads/Kourtney_beasley.pdf	9.25	0.00	\N	\N	t	f	2021-02-04 18:56:17.230355+00	2021-02-04 18:56:53.86775+00	19	ch_1IHD0aLDH0j3JuXL9BLHL8wk	\N	\N	
188	Shakari Burton	uploads/Shakari_Burton_628qWcf.pdf	9.99	0.00	\N	\N	t	f	2021-02-03 01:02:16.742866+00	2021-02-03 01:02:32.814355+00	19	ch_1IGZlLLDH0j3JuXLlv7E5eXQ	\N	kalpler beyaz gösteriyor	
190	Gerardo Sagrero	uploads/Gerardo_Sagrero.pdf	9.25	0.00	\N	\N	t	f	2021-02-03 23:17:36.057712+00	2021-02-03 23:17:47.882478+00	19	ch_1IGubVLDH0j3JuXLZXV5Hdca	\N	Font 12/Alexis Blue Thread/Angelina	
191	Latifa alhomaizi	uploads/Latifa_alhomaizi.pdf	94.25	0.00	\N	\N	t	f	2021-02-03 23:31:41.258486+00	2021-02-04 14:29:15.063407+00	19	ch_1IH8pZLDH0j3JuXLo1K86ZQH	\N	Font 18/ cream/ aspen 2021\r\nzamanında 11.02.21	
193	Savannah Newman	uploads/label_1946452513.pdf	39.98	0.00	\N	\N	f	f	2021-02-04 17:39:18.731702+00	2021-02-04 17:39:18.731719+00	20		\N	Hello,\r\nBuyer has specified the scale and size of the text. Here's the preview of the product that buyer has approved. I would be glad if you embroidered according to this image. \r\nThank you\r\nNesibe	uploads/scale.png
194	Mary Danielss	uploads/label_1946616241.pdf	9.99	0.00	\N	\N	f	f	2021-02-04 18:01:45.933123+00	2021-02-04 18:01:45.933141+00	20		\N	Hello, \r\nJust to be sure I've attached the image of the design for size and scale.\r\nThank you\r\nNesibe	uploads/lonely_hearts_copy.jpg
196	latasha		14.50	0.00	\N	\N	t	f	2021-02-04 19:39:10.689542+00	2021-02-04 19:40:13.503893+00	14	ch_1IHDgVLDH0j3JuXLQl3uSGdM	\N	\N	uploads/download-2021-02-04.pdf
197	Fanny Kuhn	uploads/Fanny_Kuhn.pdf	9.99	0.00	\N	\N	t	f	2021-02-04 20:56:25.043673+00	2021-02-04 20:56:37.678613+00	19	ch_1IHEsRLDH0j3JuXL8ArCZTAy	\N	\N	
198	Rebecca Platt	uploads/Rebecca_Platt.pdf	65.25	0.00	\N	\N	t	f	2021-02-04 21:11:36.415619+00	2021-02-04 21:11:53.440968+00	19	ch_1IHF7DLDH0j3JuXL8cSugAJx	\N	iplik rengi farklı olacak	
199	Mary Elizabeth Fagerhaugh	uploads/Mary_Elizabeth_Fagerhaugh.pdf	9.99	0.00	\N	\N	t	f	2021-02-04 21:19:57.450575+00	2021-02-04 21:20:13.810233+00	19	ch_1IHFFILDH0j3JuXLgFDmsaOz	\N	\N	
200	Ethan Viol	uploads/Ethan_Viol_label.pdf	7.25	0.00	\N	\N	t	f	2021-02-04 21:28:41.728564+00	2021-02-04 21:29:46.870508+00	19	ch_1IHFOXLDH0j3JuXLENLpQEL0	\N	Marked as gift	uploads/Ethan_Viol.pdf
201	Semyra Edu	uploads/Semyra_Edu.pdf	7.25	0.00	\N	\N	t	f	2021-02-04 21:33:53.129369+00	2021-02-04 21:34:08.377368+00	19	ch_1IHFSkLDH0j3JuXLTHW1xpQj	\N	\N	
\.


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: emre
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 201, true);


--
-- Name: orders_order orders_order_pkey; Type: CONSTRAINT; Schema: public; Owner: emre
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_pkey PRIMARY KEY (id);


--
-- Name: orders_order_coupon_id_5bddb887; Type: INDEX; Schema: public; Owner: emre
--

CREATE INDEX orders_order_coupon_id_5bddb887 ON public.orders_order USING btree (coupon_id);


--
-- Name: orders_order_ordered_by_id_ef7648ef; Type: INDEX; Schema: public; Owner: emre
--

CREATE INDEX orders_order_ordered_by_id_ef7648ef ON public.orders_order USING btree (ordered_by_id);


--
-- Name: orders_order orders_order_coupon_id_5bddb887_fk_coupons_coupon_id; Type: FK CONSTRAINT; Schema: public; Owner: emre
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_coupon_id_5bddb887_fk_coupons_coupon_id FOREIGN KEY (coupon_id) REFERENCES public.coupons_coupon(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_order orders_order_ordered_by_id_ef7648ef_fk_account_seller_id; Type: FK CONSTRAINT; Schema: public; Owner: emre
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_ordered_by_id_ef7648ef_fk_account_seller_id FOREIGN KEY (ordered_by_id) REFERENCES public.account_seller(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

