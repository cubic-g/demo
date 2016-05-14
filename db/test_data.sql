--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: address; Type: TABLE DATA; Schema: public; Owner: gcheng
--

COPY address (id, street0, street1, street2, city, province) FROM stdin;
1	6/F 9	Help St	\N	Chatswood	NSW
2	5/F 1	Railway St	\N	Chatswood	NSW
3	1	Macquarie Ln	\N	Macquarie Park	NSW
4	7	Hawk St	\N	Carlingford	NSW
\.


--
-- Name: address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gcheng
--

SELECT pg_catalog.setval('address_id_seq', 4, true);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: gcheng
--

COPY "user" (id, email, family_name, given_name) FROM stdin;
1	john.smith@hotmail.com	John	Smith
2	melissa.flynn@yahoo.com	Flynn	Melissa
\.


--
-- Data for Name: user_address; Type: TABLE DATA; Schema: public; Owner: gcheng
--

COPY user_address (user_id, address_id) FROM stdin;
1	1
1	3
2	2
2	4
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gcheng
--

SELECT pg_catalog.setval('user_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--

