INSERT INTO faqs (question, answer)
VALUES
    ('Como mejorar mi CV para ATS?', 'Evita graficos, usa texto plano, secciones claras y palabras clave del sector.'),
    ('Debo incluir foto en el CV?', 'En la mayoria de procesos ATS no es necesaria; prioriza contenido relevante.'),
    ('Cuantas paginas debe tener el CV?', '1-2 paginas es lo habitual, con foco en logros cuantificables.')
ON CONFLICT (question) DO NOTHING;
