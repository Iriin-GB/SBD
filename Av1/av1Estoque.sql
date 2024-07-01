CREATE PROCEDURE [dbo].[AtualizarSaldoEstoque]
AS
BEGIN
    DECLARE @sku VARCHAR(50)
    DECLARE @productName VARCHAR(255)
    DECLARE @qnt INT

    DECLARE stockCursor CURSOR FOR
    SELECT sku, productName, qnt
    FROM payloadEstoque;

    OPEN stockCursor;

    FETCH NEXT FROM stockCursor INTO @sku, @productName, @qnt;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        UPDATE Produto
        SET stockBalance = stockBalance + @qnt
        WHERE productName = @productName AND sku = @sku;

        FETCH NEXT FROM stockCursor INTO @sku, @productName, @qnt;
    END;

    CLOSE stockCursor;
    DEALLOCATE stockCursor;

    ;WITH CTE AS (
        SELECT *,
               ROW_NUMBER() OVER (ORDER BY stockBalance DESC) AS NumLinha
        FROM Produto
    )
    UPDATE Produto
    SET stockBalance = CTE.NumLinha
    FROM Produto
    INNER JOIN CTE ON Produto.sku = CTE.sku;

END;
