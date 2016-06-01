// Generated by CoffeeScript 1.6.2
(function() {
    (function($) {
        return $.widget('IKS.hallowagtaillink', {
            options: {
                uuid: '',
                editable: null
            },
            populateToolbar: function(toolbar) {
                var buttonSet, addButton, cancelButton, getEnclosingLink, widget;

                widget = this;
                getEnclosingLink = function() {
                    var node;

                    node = widget.options.editable.getSelection().commonAncestorContainer;
                    return $(node).parents('a').get(0);
                };

                buttonSet = $('<span class="' + this.widgetName + '"></span>');

                addButton = $('<span></span>');
                addButton = addButton.hallobutton({
                    uuid: widget.options.uuid,
                    editable: widget.options.editable,
                    label: 'Add/Edit Link',
                    icon: 'icon-link',
                    command: null,
                    queryState: function(event) {
                        return addButton.hallobutton('checked', !!getEnclosingLink());
                    }
                });
                addButton.on('click', function() {
                    var enclosingLink, lastSelection, url, urlParams, href, pageId, linkType;

                    // Defaults.
                    url = window.chooserUrls.pageChooser;
                    urlParams = {
                        'allow_external_link': true,
                        'allow_email_link': true
                    };

                    enclosingLink = getEnclosingLink();
                    lastSelection = widget.options.editable.getSelection();

                    if (enclosingLink) {
                        href = enclosingLink.getAttribute('href');
                        pageId = enclosingLink.getAttribute('data-id');
                        linkType = enclosingLink.getAttribute('data-linktype');

                        urlParams['link_text'] = enclosingLink.innerText;

                        if (linkType == 'page' && pageId) {
                            // TODO: Actually show the parent not the page itself.
                            url = window.chooserUrls.pageChooser + pageId.toString() + '/';
                        } else if (href.startsWith('mailto:')) {
                            url = window.chooserUrls.emailLinkChooser;
                            href = href.replace('mailto:', '');
                            urlParams['link_url'] = href;
                        } else if (linkType == '') {
                            url = window.chooserUrls.externalLinkChooser;
                            urlParams['link_url'] = href;
                        }
                    } else if (!lastSelection.collapsed) {
                        urlParams['link_text'] = lastSelection.toString();
                    }

                    return ModalWorkflow({
                        url: url,
                        urlParams: urlParams,
                        responses: {
                            pageChosen: function(pageData) {
                                var a, text;

                                // Create link
                                a = document.createElement('a');
                                a.setAttribute('href', pageData.url);
                                if (pageData.id) {
                                    a.setAttribute('data-id', pageData.id);
                                    a.setAttribute('data-linktype', 'page');
                                }

                                if (pageData.id) {
                                    // If it's a link to an internal page, `pageData.title` will not use the link_text
                                    // like external and email responses do, overwriting selection text :(
                                    if (!lastSelection.collapsed) {
                                        text = lastSelection.toString();
                                    } else if (enclosingLink) {
                                        text = enclosingLink.innerHTML;
                                    }
                                    else {
                                        text = pageData.title;
                                    }
                                } else {
                                    text = pageData.title;
                                }
                                a.appendChild(document.createTextNode(text));

                                // Remove existing nodes
                                if (enclosingLink && enclosingLink.parentNode) {
                                    enclosingLink.parentNode.removeChild(enclosingLink);
                                }
                                lastSelection.deleteContents();

                                // Add new node
                                lastSelection.insertNode(a);

                                return widget.options.editable.element.trigger('change');
                            }
                        }
                    });
                });
                buttonSet.append(addButton);

                cancelButton = $('<span></span>');
                cancelButton = cancelButton.hallobutton({
                    uuid: widget.options.uuid,
                    editable: widget.options.editable,
                    label: 'Remove Link',
                    icon: 'icon-chain-broken',
                    command: null,
                    queryState: function(event) {
                        if (!!getEnclosingLink()) {
                            return cancelButton.hallobutton('enable');
                        } else {
                            return cancelButton.hallobutton('disable');
                        }
                    }
                });
                cancelButton.on('click', function() {
                    var enclosingLink, sel, range;

                    enclosingLink = getEnclosingLink();
                    if (enclosingLink) {
                        sel = rangy.getSelection();
                        range = sel.getRangeAt(0);

                        range.setStartBefore(sel.anchorNode.parentNode);
                        range.setEndAfter(sel.anchorNode.parentNode);

                        sel.setSingleRange(range, false);

                        document.execCommand('unlink');
                    }
                });
                buttonSet.append(cancelButton);

                buttonSet.hallobuttonset();
                toolbar.append(buttonSet);
            }
        });
    })(jQuery);

}).call(this);
