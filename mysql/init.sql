USE blog;

-- Create the blog table
CREATE TABLE IF NOT EXISTS blog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    createdDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    createdById INT NOT NULL,
    modifiedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    modifiedById INT NOT NULL
);

-- Create the category table
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    createdDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    createdById INT NOT NULL,
    modifiedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    modifiedById INT NOT NULL
);

-- Create the blog_category junction table
CREATE TABLE IF NOT EXISTS blog_category (
    blogId INT,
    categoryId INT,
    PRIMARY KEY (blogId, categoryId),
    FOREIGN KEY (blogId) REFERENCES blog(id),
    FOREIGN KEY (categoryId) REFERENCES category(id)
);

-- Create the comment table
CREATE TABLE IF NOT EXISTS comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    blogId INT,
    content TEXT NOT NULL,
    createdDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    createdById INT NOT NULL,
    modifiedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    modifiedById INT NOT NULL,
    FOREIGN KEY (blogId) REFERENCES blog(id)
);

-- Create the blog_like table
CREATE TABLE IF NOT EXISTS blog_like (
    blogId INT,
    userId INT,
    createdDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (blogId, userId),
    FOREIGN KEY (blogId) REFERENCES blog(id)
);

-- Create the comment_like table
CREATE TABLE IF NOT EXISTS comment_like (
    commentId INT,
    userId INT,
    createdDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (commentId, userId),
    FOREIGN KEY (commentId) REFERENCES comment(id)
);

-- Insert sample data
INSERT INTO category (name, createdById, modifiedById) VALUES 
('Technology', 1, 1),
('Travel', 1, 1),
('Food', 1, 1);

INSERT INTO blog (title, content, createdById, modifiedById) VALUES 
('First Blog Post', 'This is the content of the first blog post.', 1, 1),
('Second Blog Post', 'This is the content of the second blog post.', 2, 2);

INSERT INTO blog_category (blogId, categoryId) VALUES 
(1, 1),
(2, 2);

INSERT INTO comment (blogId, content, createdById, modifiedById) VALUES 
(1, 'Great post!', 2, 2),
(1, 'I learned a lot from this.', 3, 3),
(2, 'Nice travel tips!', 1, 1);

INSERT INTO blog_like (blogId, userId) VALUES 
(1, 2),
(1, 3),
(2, 1);

INSERT INTO comment_like (commentId, userId) VALUES 
(1, 3),
(2, 1),
(3, 2);