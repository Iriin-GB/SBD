USE [GBBD];
GO

CREATE TABLE Cliente (
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    cpf VARCHAR(14),
    phone VARCHAR(20),
    CONSTRAINT PK_Cliente PRIMARY KEY (email)
);

CREATE TABLE Pedido (
    orderCode INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    orderDate DATE NOT NULL,
    recipientName VARCHAR(255),
    deliveryAddress1 VARCHAR(255),
    deliveryAddress2 VARCHAR(255),
    deliveryAddress3 VARCHAR(255),
    deliveryCity VARCHAR(255),
    deliveryState VARCHAR(255),
    deliveryPostalCode VARCHAR(20),
    deliveryCountry VARCHAR(255),
    iossNumber VARCHAR(50),
    CONSTRAINT PK_Pedido PRIMARY KEY (orderCode),
    CONSTRAINT FK_Pedido_Cliente FOREIGN KEY (email) REFERENCES Cliente (email)
);

CREATE TABLE ItemPedido (
    orderCode INT NOT NULL,
    productName VARCHAR(255) NOT NULL,
    idItemPedido INT NOT NULL,
    quantity INT NOT NULL,
    value DECIMAL(18,2) NOT NULL,
    CONSTRAINT PK_ItemPedido PRIMARY KEY (orderCode, productName),
    CONSTRAINT FK_ItemPedido_Pedido FOREIGN KEY (orderCode) REFERENCES Pedido (orderCode)
);

CREATE TABLE Produto (
    sku VARCHAR(50) NOT NULL,
    productName VARCHAR(255) NOT NULL,
    value DECIMAL(18,2) NOT NULL,
    stockBalance INT DEFAULT 0,
    CONSTRAINT PK_Produto PRIMARY KEY (sku),
    CONSTRAINT UQ_Produto_productName UNIQUE (productName)
);

CREATE TABLE Compras (
    orderCode INT NOT NULL,
    productName VARCHAR(255) NOT NULL,
    purchasedQuantity INT NOT NULL,
    CONSTRAINT PK_Compras PRIMARY KEY (orderCode, productName),
    CONSTRAINT FK_Compras_ItemPedido FOREIGN KEY (orderCode, productName) REFERENCES ItemPedido (orderCode, productName)
);

CREATE TABLE Movimentacoes (
    idMovement INT IDENTITY(1,1) PRIMARY KEY,
    orderCode INT NOT NULL,
    buyerName VARCHAR(255) NOT NULL,
    total DECIMAL(18,2) NOT NULL,
    orderComplete BIT NOT NULL,
    movementDate DATETIME DEFAULT GETDATE()
);

ALTER TABLE Produto
    ADD CONSTRAINT CHK_StockBalance_NonNegative CHECK (stockBalance >= 0);

GO

CREATE PROCEDURE [dbo].[SeparateOrderData]
AS
BEGIN
    INSERT INTO Cliente (email, name, cpf, phone)
    SELECT DISTINCT [buyer-email], [buyer-name], cpf, [buyer-phone-number]
    FROM carga
    WHERE [buyer-email] NOT IN (SELECT email FROM Cliente);

    INSERT INTO Pedido (orderCode, email, orderDate, recipientName, deliveryAddress1, deliveryAddress2, deliveryAddress3, deliveryCity, deliveryState, deliveryPostalCode, deliveryCountry, iossNumber)
    SELECT DISTINCT [order-id], [buyer-email], CONVERT(DATE, [purchase-date]) AS orderDate, 
           [recipient-name], [ship-address-1], [ship-address-2], [ship-address-3], [ship-city], [ship-state], [ship-postal-code], [ship-country], [ioss-number]
    FROM carga;

    INSERT INTO Produto (sku, productName, value, stockBalance)
    SELECT DISTINCT sku, [product-name], CONVERT(DECIMAL(18, 2), [item-price]) AS value, 10 AS stockBalance
    FROM carga
    WHERE sku NOT IN (SELECT sku FROM Produto);

    INSERT INTO ItemPedido (idItemPedido, orderCode, quantity, productName, value)
    SELECT [order-item-id], [order-id], [quantity-purchased], [product-name], CONVERT(DECIMAL(18, 2), [item-price]) AS value
    FROM carga;

    DECLARE @orderCode INT
    DECLARE @productName VARCHAR(255)
    DECLARE @quantity INT
    DECLARE @stockBalance INT
    DECLARE @orderComplete BIT
    DECLARE @totalOrder DECIMAL(18,2)
    DECLARE @totalValue DECIMAL(18,2)

    DECLARE orderCursor CURSOR FOR
    SELECT DISTINCT orderCode
    FROM ItemPedido
    ORDER BY orderCode;

    OPEN orderCursor;

    FETCH NEXT FROM orderCursor INTO @orderCode;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @totalOrder = 0;
        SET @totalValue = 0;
        SET @orderComplete = 1;

        DECLARE itemCursor CURSOR FOR
        SELECT productName, quantity
        FROM ItemPedido
        WHERE orderCode = @orderCode
        ORDER BY productName;

        OPEN itemCursor;

        FETCH NEXT FROM itemCursor INTO @productName, @quantity;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            SELECT @stockBalance = stockBalance
            FROM Produto
            WHERE productName = @productName;

            IF @stockBalance < @quantity
            BEGIN
                SET @orderComplete = 0;
                INSERT INTO Compras (orderCode, productName, purchasedQuantity)
                VALUES (@orderCode, @productName, @quantity);
            END
            ELSE
            BEGIN
                UPDATE Produto
                SET stockBalance = stockBalance - @quantity
                WHERE productName = @productName;

                SET @totalOrder = @totalOrder + @quantity;
                SET @totalValue = @totalValue + (SELECT value FROM Produto WHERE productName = @productName) * @quantity;
            END

            FETCH NEXT FROM itemCursor INTO @productName, @quantity;
        END;

        CLOSE itemCursor;
        DEALLOCATE itemCursor;

        INSERT INTO Movimentacoes (orderCode, buyerName, total, orderComplete, movementDate)
        VALUES (@orderCode, (SELECT name FROM Cliente WHERE email = (SELECT email FROM Pedido WHERE orderCode = @orderCode)), @totalValue, @orderComplete, GETDATE());

        FETCH NEXT FROM orderCursor INTO @orderCode;
    END;

    CLOSE orderCursor;
    DEALLOCATE orderCursor;

END;
