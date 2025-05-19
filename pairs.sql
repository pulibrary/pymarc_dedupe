SELECT a.id,
       row_to_json((SELECT d FROM (SELECT a.title,
                                          a.author,
                                          a.publication_year,
                                          a.pagination,
                                          a.edition,
                                          a.publisher_name,
                                          a.type_of,
                                          a.is_electronic_resource) d)),
       b.id,
       row_to_json((SELECT d FROM (SELECT b.title,
                                          b.author,
                                          b.publication_year,
                                          b.pagination,
                                          b.edition,
                                          b.publisher_name,
                                          b.type_of,
                                          b.is_electronic_resource) d))
FROM (select DISTINCT l.id AS east, r.id AS west
      FROM blocking_map AS l
      INNER JOIN blocking_map AS r
      USING (block_key)
      WHERE l.id < r.id) ids
INNER JOIN records a ON ids.east=a.id
INNER JOIN records b ON ids.west=b.id;
